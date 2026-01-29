from fastmcp import FastMCP
from .client import DatabricksClient
import json

mcp = FastMCP("databricks-resources")

@mcp.resource("databricks://clusters")
async def get_clusters_resource():
    """Resource providing cluster information"""
    async with DatabricksClient() as client:
        clusters = await client.list_clusters()
        
    # Format as NDJSON (Newline Delimited JSON)
    formatted = "\n".join(
        json.dumps({
            "id": cluster.get("cluster_id"),
            "name": cluster.get("cluster_name"),
            "state": cluster.get("state"),
            "workers": cluster.get("num_workers", 0),
            "type": cluster.get("cluster_source", "unknown")
        })
        for cluster in clusters
    )
    
    return formatted

@mcp.resource("databricks://jobs")
async def get_jobs_resource():
    """Resource providing job information"""
    async with DatabricksClient() as client:
        jobs = await client.list_jobs()
        
    formatted = "\n".join(
        json.dumps({
            "id": job.get("job_id"),
            "name": job.get("settings", {}).get("name", "Unnamed"),
            "type": job.get("settings", {}).get("type", "unknown"),
            "created_time": job.get("created_time"),
            "creator": job.get("creator_user_name")
        })
        for job in jobs
    )
    
    return formatted