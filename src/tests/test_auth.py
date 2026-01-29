import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from src.auth import DatabricksAuth

@pytest.mark.asyncio
async def test_token_validation():
    """Test token validation logic"""
    auth = DatabricksAuth()
    
    # Test valid token
    valid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE5NzI5NjQ5NjB9.dummy"
    assert auth.validate_token(valid_token) == True
    
    # Test expired token
    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjEwMDAwMDAwMDB9.dummy"
    assert auth.validate_token(expired_token) == False

@pytest.mark.asyncio
async def test_oauth_initialization():
    """Test OAuth client initialization"""
    auth = DatabricksAuth()
    
    with patch.dict('os.environ', {
        'DATABRICKS_CLIENT_ID': 'test_id',
        'DATABRICKS_CLIENT_SECRET': 'test_secret'
    }):
        await auth.initialize_oauth()
        assert auth.oauth_client is not None