from unittest.mock import AsyncMock, patch

import pytest

from ibkr.models import Order
from mcp_server.tools import (
    cancel_order,
    get_open_orders,
    modify_order,
    place_order,
    reply_to_confirmation,
)


@pytest.mark.asyncio
async def test_place_order_tool_success():
    mock_response = [{"order_id": "1001", "order_status": "submitted"}]
    with patch("mcp_server.tools.get_client") as mock_get_client:
        mock_client = AsyncMock()
        mock_client.place_orders.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        result = await place_order("U12345", 265598, "BUY", 10, "LMT", 150.0)
        assert "Order Result" in result
        assert "1001" in result

@pytest.mark.asyncio
async def test_place_order_tool_duplicate_warning():
    # T029: Test bubbling up duplicate order warnings
    mock_response = [{"warning": "Potential duplicate order", "order_id": "1002"}]
    with patch("mcp_server.tools.get_client") as mock_get_client:
        mock_client = AsyncMock()
        mock_client.place_orders.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        result = await place_order("U12345", 265598, "BUY", 10, "LMT", 150.0)
        assert "WARNING" in result
        assert "Potential duplicate" in result

@pytest.mark.asyncio
async def test_modify_order_tool():
    mock_response = {"order_id": "1001", "status": "modified"}
    with patch("mcp_server.tools.get_client") as mock_get_client:
        mock_client = AsyncMock()
        mock_client.modify_order.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        result = await modify_order("U12345", "1001", quantity=20)
        assert "Modify Result" in result
        assert "modified" in result

@pytest.mark.asyncio
async def test_cancel_order_tool():
    mock_response = {"status": "cancelled"}
    with patch("mcp_server.tools.get_client") as mock_get_client:
        mock_client = AsyncMock()
        mock_client.cancel_order.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        result = await cancel_order("U12345", "1001")
        assert "Cancel Result" in result
        assert "cancelled" in result

@pytest.mark.asyncio
async def test_get_open_orders_tool():
    mock_orders = [
        Order(
            orderId="1001",
            side="BUY",
            totalQuantity=10,
            remainingQuantity=10,
            symbol="AAPL",
            status="Submitted",
        )
    ]
    mock_response = {"orders": mock_orders}
    with patch("mcp_server.tools.get_client") as mock_get_client:
        mock_client = AsyncMock()
        mock_client.get_open_orders.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        result = await get_open_orders()
        assert "Open Orders" in result
        assert "AAPL" in result
        assert "Submitted" in result

@pytest.mark.asyncio
async def test_reply_to_confirmation_tool():
    mock_response = [{"order_id": "1001", "order_status": "submitted"}]
    with patch("mcp_server.tools.get_client") as mock_get_client:
        mock_client = AsyncMock()
        mock_client.reply_to_confirmation.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        result = await reply_to_confirmation("reply-123", True)
        assert "Reply Result" in result
        assert "submitted" in result
