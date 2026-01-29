#!/usr/bin/env python3
"""
MCP Server for Databricks Integration
"""
import asyncio
import logging
from contextlib import asynccontextmanager
from fastmcp import FastMCP
from .config import settings
from . import tools
from . import resources

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan():
    """Manage server lifecycle"""
    logger.info(f"Starting {settings.mcp_server_name} v{settings.mcp_server_version}")
    yield
    logger.info("Shutting down MCP server")

def create_app() -> FastMCP:
    """Create and configure MCP server"""
    # Create server instance
    server = FastMCP(
        name=settings.mcp_server_name,
        version=settings.mcp_server_version,
        lifespan=lifespan
    )
    
    # Import tools and resources
    # They automatically register with the server via decorators
    
    logger.info(f"MCP server created with {len(server.tools)} tools")
    return server

async def main():
    """Main entry point"""
    app = create_app()
    
    try:
        # Run the server
        await app.run()
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())