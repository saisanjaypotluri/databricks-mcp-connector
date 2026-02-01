import os
import sys

# Handle imports properly
try:
    # When running as a module
    from .client import DatabricksClient
except ImportError:
    # When running directly
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from src.client import DatabricksClient

from fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Dict

mcp = FastMCP("databricks-connector")

class SQLQueryInput(BaseModel):
    warehouse_id: str = Field(description="Databricks SQL Warehouse ID")
    query: str = Field(description="SQL query to execute")

class ClusterInput(BaseModel):
    cluster_id: str = Field(description="Databricks cluster ID")

@mcp.tool()
async def list_clusters() -> list:
    """List all Databricks clusters"""
    async with DatabricksClient() as client:
        return await client.list_clusters()

@mcp.tool()
async def get_cluster(input: ClusterInput) -> Dict:
    """Get details of a specific cluster"""
    async with DatabricksClient() as client:
        return await client.get_cluster(input.cluster_id)

@mcp.tool()
async def execute_sql(input: SQLQueryInput) -> Dict:
    """Execute SQL query on Databricks SQL warehouse"""
    async with DatabricksClient() as client:
        return await client.execute_sql(input.warehouse_id, input.query)

@mcp.tool()
async def list_jobs() -> list:
    """List all Databricks jobs"""
    async with DatabricksClient() as client:
        return await client.list_jobs()

@mcp.tool()
async def health_check() -> Dict:
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