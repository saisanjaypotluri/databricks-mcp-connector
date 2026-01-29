import pytest
import pytest_asyncio
import httpx
from unittest.mock import AsyncMock, patch, MagicMock
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.client import DatabricksClient

@pytest.fixture
def mock_auth():
    """Mock authentication"""
    with patch('src.auth.auth_manager.get_token', return_value="fake-token"):
        yield

@pytest.mark.asyncio
async def test_list_clusters(httpx_mock):
    """Test listing clusters with pytest-httpx"""
    # Mock the API response
    httpx_mock.add_response(
        method="GET",
        url="https://test.databricks.com/api/2.0/clusters/list",
        json={
            "clusters": [
                {"cluster_id": "123", "cluster_name": "test-cluster"}
            ]
        }
    )
    
    with patch('src.config.settings') as mock_settings:
        mock_settings.databricks_host = 'test.databricks.com'
        mock_settings.request_timeout = 30
        mock_settings.max_retries = 3
        
        async with DatabricksClient() as client:
            clusters = await client.list_clusters()
            assert isinstance(clusters, list)
            assert len(clusters) == 1
            assert clusters[0]["cluster_id"] == "123"

@pytest.mark.asyncio
async def test_api_error_handling(httpx_mock):
    """Test API error handling"""
    # Mock error response
    httpx_mock.add_response(
        method="GET",
        url="https://test.databricks.com/api/2.0/clusters/list",
        status_code=500,
        json={"error": "Internal Server Error"}
    )
    
    with patch('src.config.settings') as mock_settings:
        mock_settings.databricks_host = 'test.databricks.com'
        mock_settings.request_timeout = 30
        mock_settings.max_retries = 3
        
        async with DatabricksClient() as client:
            with pytest.raises(Exception) as exc_info:
                await client.list_clusters()
            assert "API Error" in str(exc_info.value)