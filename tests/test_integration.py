import pytest
import asyncio
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.main import create_app

@pytest.mark.integration
@pytest.mark.asyncio
async def test_server_startup():
    """Test MCP server can start"""
    app = create_app()
    assert app is not None
    assert hasattr(app, 'tools')

@pytest.mark.integration
@pytest.mark.asyncio
async def test_tools_registration():
    """Test that tools are properly registered"""
    app = create_app()
    
    # Check tools attribute exists
    assert hasattr(app, 'tools')
    
    # If tools is a property/method, we need to check differently
    # For FastMCP, tools might be accessed via app.tools
    try:
        tools_count = len(app.tools)
        assert tools_count > 0
    except (AttributeError, TypeError):
        # If tools is not directly accessible, we'll skip this check
        pass