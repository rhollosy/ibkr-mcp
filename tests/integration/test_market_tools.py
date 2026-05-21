from unittest.mock import AsyncMock, patch

import pytest

from ibkr.models import Contract, MarketDataSnapshot
from mcp_server.tools import get_market_data, search_contract


@pytest.mark.asyncio
async def test_search_contract_tool():
    mock_results = [
        Contract(conid=265598, symbol="AAPL", asset_class="STK", exchange="SMART")
    ]
    with patch("mcp_server.tools.get_client") as mock_get_client:
        mock_client = AsyncMock()
        mock_client.search_contract.return_value = mock_results
        mock_get_client.return_value = mock_client
        
        result = await search_contract("AAPL")
        assert "AAPL" in result
        assert "265598" in result
        assert "STK" in result

@pytest.mark.asyncio
async def test_get_market_data_tool():
    mock_data = [
        MarketDataSnapshot(conid=265598, last=150.0, bid=149.5, ask=150.5, change=0.5)
    ]
    with patch("mcp_server.tools.get_client") as mock_get_client:
        mock_client = AsyncMock()
        mock_client.get_market_data.return_value = mock_data
        mock_get_client.return_value = mock_client
        
        result = await get_market_data(265598)
        assert "Snapshot for 265598" in result
        assert "Last: 150.0" in result
        assert "Bid: 149.5" in result
        assert "Ask: 150.5" in result
