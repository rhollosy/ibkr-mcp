import os

from fastmcp import FastMCP

from ibkr.client import IBKRClient

mcp = FastMCP("IBKR Web API")

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
from . import tools


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
