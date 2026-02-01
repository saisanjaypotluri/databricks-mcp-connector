import os
import sys
import time
from typing import Optional
from authlib.integrations.httpx_client import AsyncOAuth2Client
from authlib.oauth2.rfc6749 import OAuth2Token

# Handle imports properly
try:
    # When running as a module
    from .config import settings
except ImportError:
    # When running directly
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from src.config import settings

class DatabricksAuth:
    """Handles authentication for Databricks"""
    
    def __init__(self):
        self.oauth_client = None
        self.token: Optional[OAuth2Token] = None
        self.token_expiry: float = 0
        
    async def initialize_oauth(self):
        """Initialize OAuth2 client"""
        if not settings.client_id or not settings.client_secret:
            raise ValueError("OAuth credentials not configured")
            
        self.oauth_client = AsyncOAuth2Client(
            client_id=settings.client_id,
            client_secret=settings.client_secret,
            token_endpoint=f"https://{settings.databricks_host}/oidc/v1/token",
            scope="all-apis",
        )
    
    async def get_token(self) -> str:
        """Get valid access token"""
        # For development with personal access token
        if settings.databricks_token:
            return settings.databricks_token
            
        # OAuth flow
        if not self.oauth_client:
            await self.initialize_oauth()
            
        # Get new token
        self.token = await self.oauth_client.fetch_token(
            grant_type="client_credentials"
        )
        
        # Parse expiry (usually 1 hour)
        self.token_expiry = time.time() + 3600
        
        return self.token["access_token"]
    
    def validate_token(self, token: str) -> bool:
        """Simple token validation"""
        return bool(token and len(token) > 10)

# Singleton instance
auth_manager = DatabricksAuth()