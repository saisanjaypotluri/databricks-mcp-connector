import os
import sys
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from typing import List, Dict, Any

# Handle imports properly
try:
    # When running as a module
    from .auth import auth_manager
    from .config import settings
except ImportError:
    # When running directly
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from src.auth import auth_manager
    from src.config import settings

class DatabricksClient:
    """Async HTTP client for Databricks APIs"""
    
    def __init__(self):
        self.base_url = f"https://{settings.databricks_host}/api/2.0"
        
    async def __aenter__(self):
        token = await auth_manager.get_token()
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            timeout=settings.request_timeout
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    @retry(
        stop=stop_after_attempt(settings.max_retries),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with retry logic"""
        try:
            response = await self.client.request(
                method=method,
                url=f"{self.base_url}{endpoint}",
                **kwargs
            )
            response.raise_for_status()
            return response.json() if response.content else {}
        except httpx.HTTPStatusError as e:
            error_detail = {
                "status_code": e.response.status_code,
                "error": str(e),
                "response": e.response.text[:500] if e.response.text else None
            }
            raise Exception(f"API Error: {error_detail}")
    
    async def list_clusters(self) -> List[Dict[str, Any]]:
        """List all clusters"""
        data = await self._make_request("GET", "/clusters/list")
        return data.get("clusters", [])
    
    async def execute_sql(self, warehouse_id: str, query: str) -> Dict[str, Any]:
        """Execute SQL query"""
        payload = {
            "warehouse_id": warehouse_id,
            "statement": query,
            "wait_timeout": "50s",
            "on_wait_timeout": "CANCEL"
        }
        return await self._make_request("POST", "/sql/statements", json=payload)
    
    async def get_cluster(self, cluster_id: str) -> Dict[str, Any]:
        """Get cluster details"""
        return await self._make_request("GET", f"/clusters/get?cluster_id={cluster_id}")
    
    async def list_jobs(self) -> List[Dict[str, Any]]:
        """List all jobs"""
        data = await self._make_request("GET", "/jobs/list")
        return data.get("jobs", [])