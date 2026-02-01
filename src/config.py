import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    
    databricks_host: str = Field(
        default="",
        description="Databricks workspace URL"
    )
    
    databricks_token: Optional[str] = Field(
        default=None,
        description="Personal access token"
    )
    
    client_id: Optional[str] = Field(
        default=None,
        description="OAuth client ID"
    )
    
    client_secret: Optional[str] = Field(
        default=None,
        description="OAuth client secret"
    )
    
    mcp_server_name: str = Field(
        default="databricks-connector",
        description="MCP server name"
    )
    
    request_timeout: int = Field(
        default=30,
        description="API request timeout in seconds"
    )
    
    max_retries: int = Field(
        default=3,
        description="Maximum retry attempts"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create settings instance
settings = Settings()