import pytest
import asyncio
from src.main import create_app

@pytest.mark.integration
@pytest.mark.asyncio
async def test_server_startup():
    """Test MCP server can start"""
    app = create_app()
    assert app is not None
    assert len(app.tools) > 0

@pytest.mark.integration
@pytest.mark.asyncio
async def test_tools_registration():
    """Test that tools are properly registered"""
    app = create_app()
    
    # Check specific tools are registered
    tool_names = {tool.name for tool in app.tools}
    expected_tools = {"list_clusters", "execute_sql", "check_health"}
    
    for tool in expected_tools:
        assert tool in tool_names