import os
from typing import Optional
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    
    # Databricks Configuration
    databricks_host: str = Field(
        default=os.getenv("DATABRICKS_HOST", ""),
        description="Databricks workspace URL"
    )
    databricks_token: Optional[str] = Field(
        default=os.getenv("DATABRICKS_TOKEN"),
        description="Personal access token (for development)"
    )
    
    # OAuth Configuration
    client_id: Optional[str] = Field(
        default=os.getenv("DATABRICKS_CLIENT_ID"),
        description="OAuth client ID"
    )
    client_secret: Optional[str] = Field(
        default=os.getenv("DATABRICKS_CLIENT_SECRET"),
        description="OAuth client secret"
    )
    
    # MCP Configuration
    mcp_server_name: str = Field(
        default="databricks-connector",
        description="MCP server name"
    )
    mcp_server_version: str = Field(
        default="1.0.0",
        description="MCP server version"
    )
    
    # Performance
    request_timeout: int = Field(
        default=30,
        description="API request timeout in seconds"
    )
    max_retries: int = Field(
        default=3,
        description="Maximum retry attempts for failed requests"
    )
    
    class Config:
        env_file = ".env"

settings = Settings()