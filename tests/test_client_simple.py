import pytest
import sys
import os
from unittest.mock import AsyncMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.mark.asyncio
async def test_client_list_clusters():
    """Test client list clusters"""
    from client import DatabricksClient
    
    # Mock auth manager
    with patch('client.auth_manager') as mock_auth:
        mock_auth.get_token = AsyncMock(return_value="test_token")
        
        # Mock httpx response
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={"clusters": [{"id": "cluster1"}]})
        mock_response.raise_for_status = AsyncMock()
        
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.request = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.aclose = AsyncMock()
            mock_client_class.return_value = mock_client
            
            async with DatabricksClient() as client:
                clusters = await client.list_clusters()
                assert len(clusters) == 1
                assert clusters[0]["id"] == "cluster1"

@pytest.mark.asyncio
async def test_client_execute_sql():
    """Test client SQL execution"""
    from client import DatabricksClient
    
    with patch('client.auth_manager') as mock_auth:
        mock_auth.get_token = AsyncMock(return_value="test_token")
        
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={
            "statement_id": "123",
            "status": {"state": "SUCCEEDED"}
        })
        mock_response.raise_for_status = AsyncMock()
        
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.request = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.aclose = AsyncMock()
            mock_client_class.return_value = mock_client
            
            async with DatabricksClient() as client:
                result = await client.execute_sql("warehouse1", "SELECT 1")
                assert result["statement_id"] == "123"