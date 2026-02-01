import pytest
import sys
import os
import asyncio

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Test basic imports"""
    import httpx
    import pydantic
    import asyncio
    assert True

@pytest.mark.asyncio
async def test_async_basic():
    """Test async functionality"""
    await asyncio.sleep(0.01)
    assert True

def test_config():
    """Test config module"""
    from config import settings
    assert settings is not None
    assert hasattr(settings, 'mcp_server_name')
    assert settings.mcp_server_name == "databricks-connector"
    assert hasattr(settings, 'request_timeout')
    assert settings.request_timeout == 30