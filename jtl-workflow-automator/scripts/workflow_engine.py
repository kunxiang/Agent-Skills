#!/usr/bin/env python3
"""
Workflow Engine
Base framework for orchestrating JTL business automation workflows.
"""

import json
import time
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, TypeVar
from pathlib import Path
import traceback

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

T = TypeVar("T")


class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"  # Some items succeeded, some failed
    CANCELLED = "cancelled"


class StepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class StepResult:
    """Result of a single workflow step."""
    status: StepStatus
    data: Any = None
    error: Optional[str] = None
    duration_ms: int = 0
    metadata: Dict = field(default_factory=dict)


@dataclass
class WorkflowContext:
    """Shared context passed through workflow steps."""
    workflow_id: str
    started_at: datetime = field(default_factory=datetime.now)
    data: Dict[str, Any] = field(default_factory=dict)
    step_results: Dict[str, StepResult] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    
    def set(self, key: str, value: Any):
        """Store data in context."""
        self.data[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve data from context."""
        return self.data.get(key, default)
    
    def add_error(self, error: str):
        """Record an error."""
        self.errors.append(f"[{datetime.now().isoformat()}] {error}")
        logger.error(error)


class WorkflowStep(ABC):
    """Abstract base class for workflow steps."""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, context: WorkflowContext) -> StepResult:
        """Execute the step. Override in subclasses."""
        pass
    
    def should_skip(self, context: WorkflowContext) -> bool:
        """Override to conditionally skip this step."""
        return False
    
    def on_success(self, context: WorkflowContext, result: StepResult):
        """Hook called after successful execution."""
        pass
    
    def on_failure(self, context: WorkflowContext, result: StepResult):
        """Hook called after failed execution."""
        pass


class FunctionStep(WorkflowStep):
    """Workflow step that wraps a simple function."""
    
    def __init__(
        self,
        name: str,
        func: Callable[[WorkflowContext], Any],
        description: str = "",
    ):
        super().__init__(name, description)
        self.func = func
    
    def execute(self, context: WorkflowContext) -> StepResult:
        result = self.func(context)
        return StepResult(status=StepStatus.SUCCESS, data=result)


class ConditionalStep(WorkflowStep):
    """Step that executes based on a condition."""
    
    def __init__(
        self,
        name: str,
        condition: Callable[[WorkflowContext], bool],
        if_true: WorkflowStep,
        if_false: Optional[WorkflowStep] = None,
    ):
        super().__init__(name, f"Conditional: {if_true.name}")
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false
    
    def execute(self, context: WorkflowContext) -> StepResult:
        if self.condition(context):
            return self.if_true.execute(context)
        elif self.if_false:
            return self.if_false.execute(context)
        return StepResult(status=StepStatus.SKIPPED)


class Workflow:
    """
    Main workflow orchestrator.
    
    Usage:
        workflow = Workflow("order-processing")
        workflow.add_step(FetchOrdersStep())
        workflow.add_step(ValidateOrdersStep())
        workflow.add_step(ProcessOrdersStep())
        
        result = workflow.run()
    """
    
    def __init__(
        self,
        name: str,
        description: str = "",
        fail_fast: bool = False,
        state_dir: Optional[Path] = None,
    ):
        self.name = name
        self.description = description
        self.fail_fast = fail_fast
        self.state_dir = state_dir or Path("/tmp/workflows")
        self.steps: List[WorkflowStep] = []
        self.hooks: Dict[str, List[Callable]] = {
            "before_run": [],
            "after_run": [],
            "before_step": [],
            "after_step": [],
        }
    
    def add_step(self, step: WorkflowStep) -> "Workflow":
        """Add a step to the workflow. Returns self for chaining."""
        self.steps.append(step)
        return self
    
    def add_hook(self, event: str, callback: Callable) -> "Workflow":
        """Register a hook callback."""
        if event in self.hooks:
            self.hooks[event].append(callback)
        return self
    
    def _trigger_hooks(self, event: str, *args, **kwargs):
        """Trigger all hooks for an event."""
        for hook in self.hooks.get(event, []):
            try:
                hook(*args, **kwargs)
            except Exception as e:
                logger.warning(f"Hook error ({event}): {e}")
    
    def _generate_workflow_id(self) -> str:
        """Generate unique workflow run ID."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"{self.name}-{timestamp}"
    
    def _save_state(self, context: WorkflowContext, status: WorkflowStatus):
        """Persist workflow state for recovery/audit."""
        self.state_dir.mkdir(parents=True, exist_ok=True)
        state_file = self.state_dir / f"{context.workflow_id}.json"
        
        state = {
            "workflow_id": context.workflow_id,
            "workflow_name": self.name,
            "status": status.value,
            "started_at": context.started_at.isoformat(),
            "completed_at": datetime.now().isoformat(),
            "data": {k: str(v) for k, v in context.data.items()},
            "step_results": {
                name: {
                    "status": result.status.value,
                    "duration_ms": result.duration_ms,
                    "error": result.error,
                }
                for name, result in context.step_results.items()
            },
            "errors": context.errors,
        }
        
        with open(state_file, "w") as f:
            json.dump(state, f, indent=2)
        
        logger.info(f"State saved to {state_file}")
    
    def run(self, initial_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Execute the workflow.
        
        Returns:
            Dict with keys: success, status, workflow_id, results, errors, duration_ms
        """
        workflow_id = self._generate_workflow_id()
        context = WorkflowContext(workflow_id=workflow_id)
        
        if initial_data:
            context.data.update(initial_data)
        
        logger.info(f"Starting workflow: {self.name} [{workflow_id}]")
        self._trigger_hooks("before_run", context)
        
        start_time = time.time()
        status = WorkflowStatus.RUNNING
        
        for step in self.steps:
            step_start = time.time()
            
            # Check skip condition
            if step.should_skip(context):
                result = StepResult(status=StepStatus.SKIPPED)
                context.step_results[step.name] = result
                logger.info(f"  ⏭ Skipped: {step.name}")
                continue
            
            logger.info(f"  ▶ Running: {step.name}")
            self._trigger_hooks("before_step", step, context)
            
            try:
                result = step.execute(context)
                result.duration_ms = int((time.time() - step_start) * 1000)
                
                if result.status == StepStatus.SUCCESS:
                    logger.info(f"  ✓ Completed: {step.name} ({result.duration_ms}ms)")
                    step.on_success(context, result)
                else:
                    logger.warning(f"  ✗ Failed: {step.name} - {result.error}")
                    step.on_failure(context, result)
                    
                    if self.fail_fast:
                        status = WorkflowStatus.FAILED
                        context.add_error(f"Step '{step.name}' failed: {result.error}")
                        break
                    
            except Exception as e:
                error_msg = f"{type(e).__name__}: {str(e)}"
                result = StepResult(
                    status=StepStatus.FAILED,
                    error=error_msg,
                    duration_ms=int((time.time() - step_start) * 1000),
                    metadata={"traceback": traceback.format_exc()},
                )
                logger.error(f"  ✗ Exception in {step.name}: {error_msg}")
                context.add_error(f"Step '{step.name}' raised exception: {error_msg}")
                
                if self.fail_fast:
                    status = WorkflowStatus.FAILED
                    break
            
            context.step_results[step.name] = result
            self._trigger_hooks("after_step", step, context, result)
        
        # Determine final status
        if status != WorkflowStatus.FAILED:
            failed_steps = [
                name for name, r in context.step_results.items()
                if r.status == StepStatus.FAILED
            ]
            if not failed_steps:
                status = WorkflowStatus.COMPLETED
            elif len(failed_steps) < len(context.step_results):
                status = WorkflowStatus.PARTIAL
            else:
                status = WorkflowStatus.FAILED
        
        duration_ms = int((time.time() - start_time) * 1000)
        logger.info(f"Workflow {status.value}: {self.name} [{workflow_id}] ({duration_ms}ms)")
        
        self._save_state(context, status)
        self._trigger_hooks("after_run", context, status)
        
        return {
            "success": status in (WorkflowStatus.COMPLETED, WorkflowStatus.PARTIAL),
            "status": status.value,
            "workflow_id": workflow_id,
            "results": {
                name: {
                    "status": r.status.value,
                    "data": r.data,
                    "error": r.error,
                    "duration_ms": r.duration_ms,
                }
                for name, r in context.step_results.items()
            },
            "errors": context.errors,
            "duration_ms": duration_ms,
        }


# Utility decorators for creating steps easily
def workflow_step(name: str, description: str = ""):
    """Decorator to convert a function into a WorkflowStep."""
    def decorator(func: Callable[[WorkflowContext], Any]):
        return FunctionStep(name, func, description)
    return decorator


# Example workflow
if __name__ == "__main__":
    # Demo workflow
    @workflow_step("fetch-data", "Fetch data from source")
    def fetch_data(ctx: WorkflowContext) -> dict:
        ctx.set("items", [{"id": 1, "name": "Test"}])
        return {"count": 1}
    
    @workflow_step("process-data", "Process fetched data")
    def process_data(ctx: WorkflowContext) -> dict:
        items = ctx.get("items", [])
        processed = [{"id": i["id"], "processed": True} for i in items]
        ctx.set("processed_items", processed)
        return {"processed_count": len(processed)}
    
    workflow = Workflow("demo-workflow", description="Demonstration workflow")
    workflow.add_step(fetch_data)
    workflow.add_step(process_data)
    
    result = workflow.run()
    print(json.dumps(result, indent=2))
