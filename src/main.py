#!/usr/bin/env python3
"""
MCP Server for Databricks Integration
"""
import asyncio
import logging
from fastmcp import FastMCP
from .config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Main entry point"""
    logger.info(f"Starting {settings.mcp_server_name}")
    
    # Create server instance
    server = FastMCP(
        name=settings.mcp_server_name,
        version="1.0.0"
    )
    
    # Import tools to register them
    from . import tools
    
    logger.info(f"Server created with {len(server.tools)} tools")
    
    try:
        # Run the server
        await server.run()
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())