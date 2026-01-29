import asyncio
import time
from typing import Optional, Dict, Any
from authlib.integrations.httpx_client import AsyncOAuth2Client
from authlib.oauth2.rfc6749 import OAuth2Token
from jose import jwt, JWTError
import httpx
from .config import settings

class DatabricksAuth:
    """Handles OAuth2 authentication for Databricks"""
    
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
            authorization_endpoint=f"https://{settings.databricks_host}/oidc/v1/authorize",
            scope="all-apis",
            token_endpoint_auth_method="client_secret_basic"
        )
    
    async def get_token(self) -> str:
        """Get valid access token"""
        if self.token and time.time() < self.token_expiry:
            return self.token["access_token"]
            
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
        """Validate JWT token"""
        try:
            # Decode without verification to check expiry
            decoded = jwt.get_unverified_claims(token)
            return decoded.get("exp", 0) > time.time()
        except JWTError:
            return False

# Singleton instance
auth_manager = DatabricksAuth()