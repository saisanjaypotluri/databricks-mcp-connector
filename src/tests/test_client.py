import pytest
import httpx
from unittest.mock import AsyncMock, patch
from src.client import DatabricksClient

@pytest.fixture
def mock_response():
    """Mock HTTP response"""
    response = AsyncMock()
    response.json = AsyncMock(return_value={"clusters": []})
    response.raise_for_status = AsyncMock()
    return response

@pytest.mark.asyncio
async def test_list_clusters(mock_response):
    """Test listing clusters"""
    with patch('httpx.AsyncClient.request', return_value=mock_response):
        async with DatabricksClient() as client:
            clusters = await client.list_clusters()
            assert isinstance(clusters, list)

@pytest.mark.asyncio
async def test_api_error_handling():
    """Test API error handling"""
    mock_response = AsyncMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Error", request=None, response=mock_response
    )
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    
    with patch('httpx.AsyncClient.request', return_value=mock_response):
        async with DatabricksClient() as client:
            with pytest.raises(Exception):
                await client.list_clusters()