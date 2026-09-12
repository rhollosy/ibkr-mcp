import asyncio
import logging
import os
from contextlib import asynccontextmanager, suppress

from fastmcp import FastMCP

from ibkr.client import IBKRClient

logger = logging.getLogger("mcp_server")


async def _keepalive_loop():
    """Periodically check auth status / tickle to keep the session alive."""
    logger.info("Starting IBKR keepalive background task...")
    while True:
        try:
            client = get_client()
            await client.tickle()
            logger.debug("Gateway keepalive heartbeat (tickle) sent.")
        except Exception as e:
            logger.warning(f"Error in keepalive loop: {e}")
        await asyncio.sleep(180)  # Tickle every 3 minutes


@asynccontextmanager
async def app_lifespan(_server: FastMCP):
    # Startup: spawn the keepalive background task
    keepalive_task = asyncio.create_task(_keepalive_loop())
    try:
        yield
    finally:
        # Shutdown: cancel keepalive task and close client portal connection
        logger.info("Shutting down IBKR MCP Server...")
        keepalive_task.cancel()
        with suppress(asyncio.CancelledError):
            await keepalive_task

        global _ibkr_client
        if _ibkr_client is not None:
            await _ibkr_client.close()
            _ibkr_client = None
            logger.info("IBKR Client closed successfully.")


mcp = FastMCP("IBKR Web API", lifespan=app_lifespan)

_ibkr_client: IBKRClient | None = None


def get_client() -> IBKRClient:
    global _ibkr_client
    if _ibkr_client is None:
        base_url = os.getenv("IBKR_GATEWAY_URL")
        if not base_url:
            raise ValueError("IBKR_GATEWAY_URL environment variable is not set")
        _ibkr_client = IBKRClient(base_url=base_url)
    return _ibkr_client


# Import tools here to register them with the mcp instance
from . import tools  # noqa: E402, F401


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
