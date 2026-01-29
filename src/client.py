import httpx
import asyncio
from typing import Optional, Dict, Any, List
from tenacity import retry, stop_after_attempt, wait_exponential
from .auth import auth_manager
from .config import settings

class DatabricksClient:
    """Async HTTP client for Databricks APIs"""
    
    def __init__(self):
        self.base_url = f"https://{settings.databricks_host}/api/2.0"
        self.timeout = httpx.Timeout(settings.request_timeout)
        self._client: Optional[httpx.AsyncClient] = None
        
    async def __aenter__(self):
        await self._ensure_client()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()
            
    async def _ensure_client(self):
        """Ensure HTTP client is initialized"""
        if not self._client or self._client.is_closed:
            token = await auth_manager.get_token()
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=headers,
                timeout=self.timeout,
                follow_redirects=True
            )
    
    @retry(
        stop=stop_after_attempt(settings.max_retries),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Make HTTP request with retry logic"""
        await self._ensure_client()
        
        try:
            response = await self._client.request(
                method=method,
                url=endpoint,
                **kwargs
            )
            response.raise_for_status()
            return response.json() if response.content else {}
        except httpx.HTTPStatusError as e:
            # Log error details
            error_detail = {
                "status_code": e.response.status_code,
                "error": str(e),
                "response": e.response.text[:500] if e.response.text else None
            }
            raise Exception(f"API Error: {error_detail}")
    
    # Core API Methods
    async def list_clusters(self) -> List[Dict[str, Any]]:
        """List all clusters"""
        data = await self._make_request("GET", "/clusters/list")
        return data.get("clusters", [])
    
    async def get_cluster(self, cluster_id: str) -> Dict[str, Any]:
        """Get cluster details"""
        data = await self._make_request("GET", f"/clusters/get?cluster_id={cluster_id}")
        return data
    
    async def start_cluster(self, cluster_id: str) -> Dict[str, Any]:
        """Start a cluster"""
        payload = {"cluster_id": cluster_id}
        return await self._make_request("POST", "/clusters/start", json=payload)
    
    async def list_jobs(self) -> List[Dict[str, Any]]:
        """List all jobs"""
        data = await self._make_request("GET", "/jobs/list")
        return data.get("jobs", [])
    
    async def run_job(self, job_id: int, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Run a job"""
        payload = {"job_id": job_id}
        if params:
            payload["notebook_params"] = params
        return await self._make_request("POST", "/jobs/run-now", json=payload)
    
    async def execute_sql(
        self,
        warehouse_id: str,
        query: str,
        parameters: Optional[List] = None
    ) -> Dict[str, Any]:
        """Execute SQL query on Databricks SQL warehouse"""
        payload = {
            "warehouse_id": warehouse_id,
            "statement": query,
            "wait_timeout": "50s",
            "on_wait_timeout": "CANCEL"
        }
        if parameters:
            payload["parameters"] = parameters
            
        return await self._make_request("POST", "/sql/statements", json=payload)