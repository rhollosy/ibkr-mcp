from unittest.mock import AsyncMock, patch

import pytest

from ibkr.exceptions import RequestError
from mcp_server.tools import (
    cancel_order,
    get_account_summary,
    get_accounts,
    get_market_data,
    get_open_orders,
    get_positions,
    modify_order,
    place_order,
    reply_to_confirmation,
    search_contract,
)


@pytest.fixture
def mock_error_client():
    with patch("mcp_server.tools.get_client") as mock:
        client = AsyncMock()
        mock.return_value = client
        yield client

@pytest.mark.asyncio
async def test_get_accounts_error(mock_error_client):
    mock_error_client.get_accounts.side_effect = RequestError("Fail")
    assert "Error: Fail" in await get_accounts()

@pytest.mark.asyncio
async def test_get_account_summary_error(mock_error_client):
    mock_error_client.get_account_summary.side_effect = RequestError("Fail")
    assert "Error: Fail" in await get_account_summary("U1")

@pytest.mark.asyncio
async def test_get_positions_error(mock_error_client):
    mock_error_client.get_positions.side_effect = RequestError("Fail")
    assert "Error: Fail" in await get_positions("U1")

@pytest.mark.asyncio
async def test_search_contract_error(mock_error_client):
    mock_error_client.search_contract.side_effect = RequestError("Fail")
    assert "Error: Fail" in await search_contract("AAPL")

@pytest.mark.asyncio
async def test_get_market_data_error(mock_error_client):
    mock_error_client.get_market_data.side_effect = RequestError("Fail")
    assert "Error: Fail" in await get_market_data(123)

@pytest.mark.asyncio
async def test_place_order_error(mock_error_client):
    mock_error_client.place_orders.side_effect = RequestError("Fail")
    assert "Error: Fail" in await place_order("U1", 123, "BUY", 10, "LMT")

@pytest.mark.asyncio
async def test_modify_order_error(mock_error_client):
    mock_error_client.modify_order.side_effect = RequestError("Fail")
    assert "Error: Fail" in await modify_order("U1", "O1")

@pytest.mark.asyncio
async def test_cancel_order_error(mock_error_client):
    mock_error_client.cancel_order.side_effect = RequestError("Fail")
    assert "Error: Fail" in await cancel_order("U1", "O1")

@pytest.mark.asyncio
async def test_get_open_orders_error(mock_error_client):
    mock_error_client.get_open_orders.side_effect = RequestError("Fail")
    assert "Error: Fail" in await get_open_orders()

@pytest.mark.asyncio
async def test_reply_to_confirmation_error(mock_error_client):
    mock_error_client.reply_to_confirmation.side_effect = RequestError("Fail")
    assert "Error: Fail" in await reply_to_confirmation("R1", True)
