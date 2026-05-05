from unittest.mock import AsyncMock, patch

import pytest

from mcp_server.tools import get_account_summary, get_accounts, get_positions


@pytest.mark.asyncio
async def test_get_accounts_tool():
    mock_accounts = [{"accountId": "U12345", "accountName": "Individual"}]
    with patch("mcp_server.tools.get_client") as mock_get_client:
        mock_client = AsyncMock()
        mock_client.get_accounts.return_value = mock_accounts
        mock_get_client.return_value = mock_client
        
        result = await get_accounts()
        assert "U12345" in result
        assert "Individual" in result

@pytest.mark.asyncio
async def test_get_account_summary_tool():
    mock_summary = {"NetLiquidation": 100000.0, "Currency": "USD"}
    with patch("mcp_server.tools.get_client") as mock_get_client:
        mock_client = AsyncMock()
        mock_client.get_account_summary.return_value = mock_summary
        mock_get_client.return_value = mock_client
        
        result = await get_account_summary("U12345")
        assert "Summary for U12345" in result
        assert "NetLiquidation: 100000.0" in result

@pytest.mark.asyncio
async def test_get_positions_tool():
    mock_positions = [
        {"symbol": "AAPL", "conid": 265598, "position": 100, "avgPrice": 150.0, "mktPrice": 155.0}
    ]
    with patch("mcp_server.tools.get_client") as mock_get_client:
        mock_client = AsyncMock()
        mock_client.get_positions.return_value = mock_positions
        mock_get_client.return_value = mock_client
        
        result = await get_positions("U12345")
        assert "AAPL" in result
        assert "100" in result
        assert "150.0" in result
