from unittest.mock import MagicMock

import httpx
import pytest

from ibkr.exceptions import AuthenticationError, GatewayTimeoutError, RequestError


@pytest.mark.asyncio
async def test_request_success(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "ok"}
    mock_client.client.request.return_value = mock_response

    result = await mock_client._request("GET", "/test")
    assert result == {"data": "ok"}

@pytest.mark.asyncio
async def test_request_auth_error(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_client.client.request.side_effect = httpx.HTTPStatusError(
        "Unauthorized", request=MagicMock(), response=mock_response
    )

    with pytest.raises(AuthenticationError):
        await mock_client._request("GET", "/test")

@pytest.mark.asyncio
async def test_request_timeout_error(mock_client):
    mock_client.client.request.side_effect = httpx.ConnectError(
        "Timeout", request=MagicMock()
    )

    with pytest.raises(GatewayTimeoutError):
        await mock_client._request("GET", "/test")

@pytest.mark.asyncio
async def test_request_generic_error(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_client.client.request.side_effect = httpx.HTTPStatusError(
        "Internal Server Error", request=MagicMock(), response=mock_response
    )

    with pytest.raises(RequestError):
        await mock_client._request("GET", "/test")

@pytest.mark.asyncio
async def test_get_auth_status(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"authenticated": True}
    mock_client.client.request.return_value = mock_response

    status = await mock_client.get_auth_status()
    assert status["authenticated"] is True

@pytest.mark.asyncio
async def test_get_accounts(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"accountId": "U1"}]
    mock_client.client.request.return_value = mock_response

    accounts = await mock_client.get_accounts()
    assert accounts[0].id == "U1"


@pytest.mark.asyncio
async def test_get_account_summary(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"NetLiquidation": 100}
    mock_client.client.request.return_value = mock_response

    summary = await mock_client.get_account_summary("U1")
    assert summary["NetLiquidation"] == 100


@pytest.mark.asyncio
async def test_get_positions(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"symbol": "AAPL"}]
    mock_client.client.request.return_value = mock_response

    positions = await mock_client.get_positions("U1")
    assert positions[0].symbol == "AAPL"


@pytest.mark.asyncio
async def test_search_contract(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"conid": 123}]
    mock_client.client.request.return_value = mock_response

    results = await mock_client.search_contract("AAPL")
    assert results[0].conid == 123


@pytest.mark.asyncio
async def test_get_market_data(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"31": 150}]
    mock_client.client.request.return_value = mock_response

    data = await mock_client.get_market_data([123])
    assert data[0].last == 150.0


@pytest.mark.asyncio
async def test_place_orders(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"orderId": "O1"}]
    mock_client.client.request.return_value = mock_response

    res = await mock_client.place_orders("U1", [{"conid": 123}])
    assert res[0]["orderId"] == "O1"


@pytest.mark.asyncio
async def test_modify_order(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "ok"}
    mock_client.client.request.return_value = mock_response

    res = await mock_client.modify_order("U1", "O1", {"quantity": 20})
    assert res["status"] == "ok"


@pytest.mark.asyncio
async def test_cancel_order(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "ok"}
    mock_client.client.request.return_value = mock_response

    res = await mock_client.cancel_order("U1", "O1")
    assert res["status"] == "ok"


@pytest.mark.asyncio
async def test_get_open_orders(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"orders": []}
    mock_client.client.request.return_value = mock_response

    res = await mock_client.get_open_orders()
    assert res["orders"] == []


@pytest.mark.asyncio
async def test_reply_to_confirmation(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"orderId": "O1"}]
    mock_client.client.request.return_value = mock_response

    res = await mock_client.reply_to_confirmation("reply_123", True)
    assert res[0]["orderId"] == "O1"
