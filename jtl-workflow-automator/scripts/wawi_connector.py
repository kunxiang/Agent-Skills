#!/usr/bin/env python3
"""
JTL-Wawi REST API Connector
Handles authentication, requests, and response parsing for JTL-Wawi API.
"""

import os
import time
import json
import hashlib
import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class WawiConfig:
    """Configuration for JTL-Wawi API connection."""
    base_url: str  # e.g., "https://your-wawi-server:port"
    app_id: str
    api_key: str
    timeout: int = 30
    max_retries: int = 3
    
    @classmethod
    def from_env(cls) -> "WawiConfig":
        """Load configuration from environment variables."""
        return cls(
            base_url=os.environ["JTL_WAWI_URL"],
            app_id=os.environ["JTL_WAWI_APP_ID"],
            api_key=os.environ["JTL_WAWI_API_KEY"],
            timeout=int(os.environ.get("JTL_WAWI_TIMEOUT", "30")),
            max_retries=int(os.environ.get("JTL_WAWI_MAX_RETRIES", "3")),
        )


class WawiConnector:
    """
    JTL-Wawi REST API client with authentication and error handling.
    
    Usage:
        config = WawiConfig.from_env()
        connector = WawiConnector(config)
        
        # Get all articles
        articles = connector.get("/v1/articles")
        
        # Create an order
        order = connector.post("/v1/orders", data=order_data)
        
        # Batch operations
        results = connector.batch_get("/v1/articles", ids=[1, 2, 3])
    """
    
    def __init__(self, config: WawiConfig):
        self.config = config
        self.session = requests.Session()
        self._setup_auth()
    
    def _setup_auth(self):
        """Configure session with API authentication headers."""
        self.session.headers.update({
            "X-AppId": self.config.app_id,
            "X-ApiKey": self.config.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        correlation_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Execute API request with retry logic and error handling."""
        url = f"{self.config.base_url}{endpoint}"
        correlation_id = correlation_id or self._generate_correlation_id()
        
        headers = {"X-Correlation-Id": correlation_id}
        
        for attempt in range(self.config.max_retries):
            try:
                logger.info(f"[{correlation_id}] {method} {endpoint} (attempt {attempt + 1})")
                
                response = self.session.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    headers=headers,
                    timeout=self.config.timeout,
                )
                
                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    logger.warning(f"[{correlation_id}] Rate limited, waiting {retry_after}s")
                    time.sleep(retry_after)
                    continue
                
                response.raise_for_status()
                
                return {
                    "success": True,
                    "data": response.json() if response.text else None,
                    "correlation_id": correlation_id,
                    "status_code": response.status_code,
                }
                
            except requests.exceptions.Timeout:
                logger.warning(f"[{correlation_id}] Timeout on attempt {attempt + 1}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                    
            except requests.exceptions.HTTPError as e:
                error_detail = self._parse_error(e.response)
                logger.error(f"[{correlation_id}] HTTP Error: {error_detail}")
                return {
                    "success": False,
                    "error": error_detail,
                    "correlation_id": correlation_id,
                    "status_code": e.response.status_code,
                }
                
            except requests.exceptions.RequestException as e:
                logger.error(f"[{correlation_id}] Request failed: {str(e)}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
        
        return {
            "success": False,
            "error": "Max retries exceeded",
            "correlation_id": correlation_id,
        }
    
    def _parse_error(self, response: requests.Response) -> str:
        """Extract error message from API response."""
        try:
            error_data = response.json()
            return error_data.get("message", error_data.get("error", str(response.text)))
        except json.JSONDecodeError:
            return response.text or f"HTTP {response.status_code}"
    
    def _generate_correlation_id(self) -> str:
        """Generate unique correlation ID for request tracking."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_part = hashlib.md5(os.urandom(8)).hexdigest()[:8]
        return f"wawi-{timestamp}-{random_part}"
    
    # Convenience methods
    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> Dict:
        return self._make_request("GET", endpoint, params=params, **kwargs)
    
    def post(self, endpoint: str, data: Dict, **kwargs) -> Dict:
        return self._make_request("POST", endpoint, data=data, **kwargs)
    
    def put(self, endpoint: str, data: Dict, **kwargs) -> Dict:
        return self._make_request("PUT", endpoint, data=data, **kwargs)
    
    def patch(self, endpoint: str, data: Dict, **kwargs) -> Dict:
        return self._make_request("PATCH", endpoint, data=data, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> Dict:
        return self._make_request("DELETE", endpoint, **kwargs)
    
    # Batch operations
    def batch_get(
        self,
        endpoint: str,
        ids: List[int],
        id_param: str = "id",
        batch_size: int = 50,
    ) -> List[Dict]:
        """Fetch multiple items by ID in batches."""
        results = []
        for i in range(0, len(ids), batch_size):
            batch_ids = ids[i:i + batch_size]
            response = self.get(endpoint, params={id_param: ",".join(map(str, batch_ids))})
            if response["success"] and response.get("data"):
                results.extend(response["data"] if isinstance(response["data"], list) else [response["data"]])
        return results
    
    # Common API endpoints
    def get_articles(self, page: int = 1, limit: int = 100, **filters) -> Dict:
        """Fetch articles with pagination and filters."""
        params = {"page": page, "limit": limit, **filters}
        return self.get("/v1/articles", params=params)
    
    def get_orders(self, status: Optional[str] = None, since: Optional[datetime] = None) -> Dict:
        """Fetch orders with optional filters."""
        params = {}
        if status:
            params["status"] = status
        if since:
            params["modifiedSince"] = since.isoformat()
        return self.get("/v1/orders", params=params)
    
    def get_customers(self, page: int = 1, limit: int = 100) -> Dict:
        """Fetch customers with pagination."""
        return self.get("/v1/customers", params={"page": page, "limit": limit})
    
    def update_stock(self, article_id: int, stock_data: Dict) -> Dict:
        """Update stock levels for an article."""
        return self.patch(f"/v1/articles/{article_id}/stock", data=stock_data)
    
    def create_order(self, order_data: Dict) -> Dict:
        """Create a new order."""
        return self.post("/v1/orders", data=order_data)


# Example usage
if __name__ == "__main__":
    # Demo with mock config
    config = WawiConfig(
        base_url="https://localhost:8080",
        app_id="demo-app",
        api_key="demo-key",
    )
    connector = WawiConnector(config)
    print("WawiConnector initialized successfully")
    print(f"Base URL: {config.base_url}")
