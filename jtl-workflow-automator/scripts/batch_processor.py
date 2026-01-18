#!/usr/bin/env python3
"""
Batch Processor
Parallel batch processing for large JTL datasets with progress tracking and error handling.
"""

import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, Generic, Iterator, List, Optional, TypeVar
from enum import Enum

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

T = TypeVar("T")
R = TypeVar("R")


class ItemStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class ProcessedItem(Generic[T, R]):
    """Result of processing a single item."""
    item: T
    status: ItemStatus
    result: Optional[R] = None
    error: Optional[str] = None
    attempts: int = 1
    duration_ms: int = 0


@dataclass
class BatchResult(Generic[T, R]):
    """Result of processing a batch."""
    total: int
    succeeded: int
    failed: int
    skipped: int
    items: List[ProcessedItem[T, R]]
    duration_ms: int
    errors: List[str] = field(default_factory=list)
    
    @property
    def success_rate(self) -> float:
        return (self.succeeded / self.total * 100) if self.total > 0 else 0.0
    
    def to_dict(self) -> Dict:
        return {
            "total": self.total,
            "succeeded": self.succeeded,
            "failed": self.failed,
            "skipped": self.skipped,
            "success_rate": f"{self.success_rate:.1f}%",
            "duration_ms": self.duration_ms,
            "errors": self.errors[:10],  # Limit error list
        }


class BatchProcessor(Generic[T, R]):
    """
    Process large datasets in parallel batches with retry logic.
    
    Usage:
        processor = BatchProcessor(
            process_func=lambda item: api.update(item),
            batch_size=50,
            max_workers=4,
        )
        
        result = processor.process(items)
        print(f"Processed {result.succeeded}/{result.total} items")
    """
    
    def __init__(
        self,
        process_func: Callable[[T], R],
        batch_size: int = 100,
        max_workers: int = 4,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        skip_condition: Optional[Callable[[T], bool]] = None,
        on_item_complete: Optional[Callable[[ProcessedItem[T, R]], None]] = None,
        on_batch_complete: Optional[Callable[[int, int, int], None]] = None,
    ):
        self.process_func = process_func
        self.batch_size = batch_size
        self.max_workers = max_workers
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.skip_condition = skip_condition
        self.on_item_complete = on_item_complete
        self.on_batch_complete = on_batch_complete
    
    def _chunk_items(self, items: List[T]) -> Iterator[List[T]]:
        """Split items into batches."""
        for i in range(0, len(items), self.batch_size):
            yield items[i:i + self.batch_size]
    
    def _process_single(self, item: T) -> ProcessedItem[T, R]:
        """Process a single item with retry logic."""
        start_time = time.time()
        
        # Check skip condition
        if self.skip_condition and self.skip_condition(item):
            return ProcessedItem(
                item=item,
                status=ItemStatus.SKIPPED,
                duration_ms=0,
            )
        
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                result = self.process_func(item)
                duration_ms = int((time.time() - start_time) * 1000)
                
                return ProcessedItem(
                    item=item,
                    status=ItemStatus.SUCCESS,
                    result=result,
                    attempts=attempt,
                    duration_ms=duration_ms,
                )
                
            except Exception as e:
                last_error = str(e)
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * attempt)  # Exponential backoff
        
        duration_ms = int((time.time() - start_time) * 1000)
        return ProcessedItem(
            item=item,
            status=ItemStatus.FAILED,
            error=last_error,
            attempts=self.max_retries,
            duration_ms=duration_ms,
        )
    
    def process(self, items: List[T]) -> BatchResult[T, R]:
        """Process all items in parallel batches."""
        start_time = time.time()
        all_results: List[ProcessedItem[T, R]] = []
        errors: List[str] = []
        
        total_batches = (len(items) + self.batch_size - 1) // self.batch_size
        
        logger.info(f"Processing {len(items)} items in {total_batches} batches "
                   f"({self.max_workers} workers, batch size {self.batch_size})")
        
        for batch_num, batch in enumerate(self._chunk_items(items), 1):
            batch_start = time.time()
            batch_results: List[ProcessedItem[T, R]] = []
            
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {
                    executor.submit(self._process_single, item): item
                    for item in batch
                }
                
                for future in as_completed(futures):
                    result = future.result()
                    batch_results.append(result)
                    
                    if result.status == ItemStatus.FAILED:
                        errors.append(f"Item failed: {result.error}")
                    
                    if self.on_item_complete:
                        self.on_item_complete(result)
            
            all_results.extend(batch_results)
            
            succeeded = sum(1 for r in batch_results if r.status == ItemStatus.SUCCESS)
            failed = sum(1 for r in batch_results if r.status == ItemStatus.FAILED)
            
            batch_duration = int((time.time() - batch_start) * 1000)
            logger.info(f"Batch {batch_num}/{total_batches}: "
                       f"{succeeded} succeeded, {failed} failed ({batch_duration}ms)")
            
            if self.on_batch_complete:
                self.on_batch_complete(batch_num, total_batches, len(batch))
        
        duration_ms = int((time.time() - start_time) * 1000)
        
        return BatchResult(
            total=len(items),
            succeeded=sum(1 for r in all_results if r.status == ItemStatus.SUCCESS),
            failed=sum(1 for r in all_results if r.status == ItemStatus.FAILED),
            skipped=sum(1 for r in all_results if r.status == ItemStatus.SKIPPED),
            items=all_results,
            duration_ms=duration_ms,
            errors=errors,
        )
    
    def process_with_progress(
        self,
        items: List[T],
        progress_callback: Callable[[int, int], None],
    ) -> BatchResult[T, R]:
        """Process with progress updates."""
        processed_count = 0
        total = len(items)
        
        def on_complete(item: ProcessedItem):
            nonlocal processed_count
            processed_count += 1
            progress_callback(processed_count, total)
        
        original_callback = self.on_item_complete
        self.on_item_complete = on_complete
        
        try:
            result = self.process(items)
        finally:
            self.on_item_complete = original_callback
        
        return result


# Convenience function for simple batch processing
def batch_process(
    items: List[T],
    process_func: Callable[[T], R],
    batch_size: int = 100,
    max_workers: int = 4,
) -> BatchResult[T, R]:
    """Simple batch processing without creating a processor instance."""
    processor = BatchProcessor(
        process_func=process_func,
        batch_size=batch_size,
        max_workers=max_workers,
    )
    return processor.process(items)


# Example usage
if __name__ == "__main__":
    import random
    
    # Simulated processing function
    def process_item(item: dict) -> dict:
        time.sleep(random.uniform(0.1, 0.3))  # Simulate API call
        if random.random() < 0.1:  # 10% failure rate
            raise Exception("Random failure")
        return {"id": item["id"], "processed": True}
    
    # Create test items
    items = [{"id": i, "name": f"Item {i}"} for i in range(25)]
    
    # Process with progress
    def show_progress(current: int, total: int):
        percent = current / total * 100
        print(f"\rProgress: {current}/{total} ({percent:.0f}%)", end="", flush=True)
    
    processor = BatchProcessor(
        process_func=process_item,
        batch_size=10,
        max_workers=3,
        max_retries=2,
    )
    
    result = processor.process_with_progress(items, show_progress)
    print()  # New line after progress
    print(f"\nResults: {result.to_dict()}")
