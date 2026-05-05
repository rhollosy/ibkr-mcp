from unittest.mock import AsyncMock, patch

import pytest

from mcp_server.tools import get_market_data, search_contract


@pytest.mark.asyncio
async def test_search_contract_tool():
    mock_results = [{"symbol": "AAPL", "conid": 265598, "assetClass": "STK", "exchange": "SMART"}]
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
    mock_data = [{"conid": 265598, "31": 150.0, "84": 149.5, "86": 150.5, "82": 0.5}]
    with patch("mcp_server.tools.get_client") as mock_get_client:
        mock_client = AsyncMock()
        mock_client.get_market_data.return_value = mock_data
        mock_get_client.return_value = mock_client
        
        result = await get_market_data(265598)
        assert "Snapshot for 265598" in result
        assert "Last: 150.0" in result
        assert "Bid: 149.5" in result
        assert "Ask: 150.5" in result
