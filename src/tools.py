from typing import Optional, List, Dict, Any
from fastmcp import FastMCP
from pydantic import BaseModel, Field
from .client import DatabricksClient

# Initialize MCP server
mcp = FastMCP("databricks-connector")

# Pydantic models for tool inputs
class SQLQueryInput(BaseModel):
    warehouse_id: str = Field(description="Databricks SQL Warehouse ID")
    query: str = Field(description="SQL query to execute")
    parameters: Optional[List[Any]] = Field(
        default=None,
        description="Query parameters"
    )

class ClusterActionInput(BaseModel):
    cluster_id: str = Field(description="Databricks cluster ID")

class RunJobInput(BaseModel):
    job_id: int = Field(description="Databricks job ID")
    params: Optional[Dict[str, str]] = Field(
        default=None,
        description="Job parameters"
    )

@mcp.tool()
async def list_clusters() -> List[Dict[str, Any]]:
    """List all Databricks clusters"""
    async with DatabricksClient() as client:
        return await client.list_clusters()

@mcp.tool()
async def get_cluster(cluster_id: str) -> Dict[str, Any]:
    """Get details of a specific cluster"""
    async with DatabricksClient() as client:
        return await client.get_cluster(cluster_id)

@mcp.tool()
async def start_cluster(input: ClusterActionInput) -> Dict[str, Any]:
    """Start a Databricks cluster"""
    async with DatabricksClient() as client:
        return await client.start_cluster(input.cluster_id)

@mcp.tool()
async def stop_cluster(input: ClusterActionInput) -> Dict[str, Any]:
    """Stop a Databricks cluster"""
    async with DatabricksClient() as client:
        # Note: You'll need to add stop_cluster method to client
        return {"status": "Not implemented yet"}

@mcp.tool()
async def list_jobs() -> List[Dict[str, Any]]:
    """List all Databricks jobs"""
    async with DatabricksClient() as client:
        return await client.list_jobs()

@mcp.tool()
async def run_job(input: RunJobInput) -> Dict[str, Any]:
    """Run a Databricks job"""
    async with DatabricksClient() as client:
        return await client.run_job(input.job_id, input.params)

@mcp.tool()
async def execute_sql(input: SQLQueryInput) -> Dict[str, Any]:
    """Execute SQL query on Databricks SQL warehouse"""
    async with DatabricksClient() as client:
        return await client.execute_sql(
            input.warehouse_id,
            input.query,
            input.parameters
        )

@mcp.tool()
async def check_health() -> Dict[str, Any]:
    """Check connection health to Databricks"""
    try:
        async with DatabricksClient() as client:
            clusters = await client.list_clusters()
            return {
                "status": "healthy",
                "clusters_count": len(clusters),
                "message": "Successfully connected to Databricks"
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "message": "Failed to connect to Databricks"
        }