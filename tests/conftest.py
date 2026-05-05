from unittest.mock import AsyncMock, patch

import pytest_asyncio

from ibkr.client import IBKRClient


@pytest_asyncio.fixture
async def mock_client():
    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        client = IBKRClient(base_url="https://mock-gateway/v1/api")
        # Ensure the client uses the patched request
        yield client
