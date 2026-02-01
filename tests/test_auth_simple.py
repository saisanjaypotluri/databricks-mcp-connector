import pytest
import sys
import os
from unittest.mock import AsyncMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.mark.asyncio
async def test_auth_token():
    """Test authentication token retrieval"""
    from auth import DatabricksAuth
    
    auth = DatabricksAuth()
    
    # Mock settings
    with patch('auth.settings') as mock_settings:
        mock_settings.databricks_token = "test_token_1234567890"
        
        token = await auth.get_token()
        assert token == "test_token_1234567890"

@pytest.mark.asyncio
async def test_oauth_initialization():
    """Test OAuth initialization"""
    from auth import DatabricksAuth
    
    auth = DatabricksAuth()
    
    with patch('auth.settings') as mock_settings:
        mock_settings.databricks_token = None
        mock_settings.client_id = "test_id"
        mock_settings.client_secret = "test_secret"
        mock_settings.databricks_host = "test.cloud.databricks.com"
        
        # Mock AsyncOAuth2Client
        with patch('auth.AsyncOAuth2Client') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.fetch_token = AsyncMock(return_value={"access_token": "oauth_token"})
            mock_client_class.return_value = mock_client
            
            await auth.initialize_oauth()
            assert auth.oauth_client is not None