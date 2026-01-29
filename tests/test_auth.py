import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Now import from src
from src.auth import DatabricksAuth
import time

@pytest.mark.asyncio
async def test_token_validation():
    """Test token validation logic"""
    auth = DatabricksAuth()
    
    # Test with mocked JWT validation
    with patch('src.auth.jwt.get_unverified_claims') as mock_jwt:
        mock_jwt.side_effect = Exception("Test exception")
        # Since we can't create valid JWTs easily, we'll test the error path
        assert not auth.validate_token("invalid-token")

@pytest.mark.asyncio
async def test_get_token_with_pat():
    """Test getting token with personal access token"""
    auth = DatabricksAuth()
    
    # Test with PAT
    with patch('src.config.settings') as mock_settings:
        mock_settings.databricks_token = 'test-pat-token'
        mock_settings.client_id = None
        mock_settings.client_secret = None
        token = await auth.get_token()
        assert token == "test-pat-token"

@pytest.mark.asyncio
async def test_oauth_flow():
    """Test OAuth flow initialization"""
    auth = DatabricksAuth()
    
    # Mock AsyncOAuth2Client
    mock_oauth_client = AsyncMock()
    mock_oauth_client.fetch_token = AsyncMock(
        return_value={"access_token": "test-oauth-token", "expires_in": 3600}
    )
    
    with patch('src.auth.AsyncOAuth2Client', return_value=mock_oauth_client):
        with patch('src.config.settings') as mock_settings:
            mock_settings.client_id = 'test-client-id'
            mock_settings.client_secret = 'test-client-secret'
            mock_settings.databricks_host = 'test.databricks.com'
            mock_settings.databricks_token = None
            
            await auth.initialize_oauth()
            assert auth.oauth_client is not None
            
            # Test token fetching
            token = await auth.get_token()
            assert token == "test-oauth-token"