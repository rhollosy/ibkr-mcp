from unittest.mock import AsyncMock, patch

import pytest

from mcp_server.tools import get_auth_status


@pytest.mark.asyncio
async def test_get_auth_status_tool_authenticated():
    mock_status = {"authenticated": True, "connected": True}
    with patch("mcp_server.tools.get_client") as mock_get_client:
        mock_client = AsyncMock()
        mock_client.get_auth_status.return_value = mock_status
        mock_get_client.return_value = mock_client
        
        result = await get_auth_status()
        assert "Authenticated" in result
        assert "Gateway is connected" in result

@pytest.mark.asyncio
async def test_get_auth_status_tool_unauthenticated():
    mock_status = {"authenticated": False}
    with patch("mcp_server.tools.get_client") as mock_get_client:
        mock_client = AsyncMock()
        mock_client.base_url = "https://mock-gateway/v1/api"
        mock_client.get_auth_status.return_value = mock_status
        mock_get_client.return_value = mock_client
        
        result = await get_auth_status()
        assert "Unauthenticated" in result
        assert "log in via the IBKR Gateway UI" in result

@pytest.mark.asyncio
async def test_get_auth_status_tool_error():
    from ibkr.exceptions import RequestError
    with patch("mcp_server.tools.get_client") as mock_get_client:
        mock_client = AsyncMock()
        mock_client.get_auth_status.side_effect = RequestError("Connection failed")
        mock_get_client.return_value = mock_client
        
        result = await get_auth_status()
        assert "Error" in result
        assert "Connection failed" in result
