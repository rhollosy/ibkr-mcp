import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import main as main_entry
from mcp_server.server import _keepalive_loop, app_lifespan, get_client, main


def test_get_client_no_env(monkeypatch):
    monkeypatch.delenv("IBKR_GATEWAY_URL", raising=False)
    # Clear the global client cached state
    import mcp_server.server
    mcp_server.server._ibkr_client = None
    match_msg = "IBKR_GATEWAY_URL environment variable is not set"
    with pytest.raises(ValueError, match=match_msg):
        get_client()


def test_get_client_with_env(monkeypatch):
    monkeypatch.setenv("IBKR_GATEWAY_URL", "https://localhost:5000/v1/api")
    import mcp_server.server
    mcp_server.server._ibkr_client = None
    client = get_client()
    assert client.base_url == "https://localhost:5000/v1/api"
    # calling again returns same client
    assert get_client() is client
    # Clean up
    mcp_server.server._ibkr_client = None


@pytest.mark.asyncio
async def test_keepalive_loop():
    import mcp_server.server
    mock_client = AsyncMock()
    mcp_server.server._ibkr_client = mock_client
    
    with patch("asyncio.sleep", side_effect=[asyncio.CancelledError]) as mock_sleep:
        with pytest.raises(asyncio.CancelledError):
            await _keepalive_loop()
        
        mock_client.tickle.assert_called_once()
        mock_sleep.assert_any_call(180)
    mcp_server.server._ibkr_client = None


@pytest.mark.asyncio
async def test_keepalive_loop_exception():
    import mcp_server.server
    mock_client = AsyncMock()
    mock_client.tickle.side_effect = Exception("HTTP failure")
    mcp_server.server._ibkr_client = mock_client
    
    with patch("asyncio.sleep", side_effect=[asyncio.CancelledError]):
        with pytest.raises(asyncio.CancelledError):
            await _keepalive_loop()
        
        mock_client.tickle.assert_called_once()
    mcp_server.server._ibkr_client = None


@pytest.mark.asyncio
async def test_app_lifespan():
    import mcp_server.server
    mock_client = AsyncMock()
    mcp_server.server._ibkr_client = mock_client
    
    # We mock _keepalive_loop to return immediately
    with patch(
        "mcp_server.server._keepalive_loop", new_callable=AsyncMock
    ):
        mock_mcp = MagicMock()
        async with app_lifespan(mock_mcp):
            pass
            
        mock_client.close.assert_called_once()
        assert mcp_server.server._ibkr_client is None


def test_server_main():
    with patch("mcp_server.server.mcp.run") as mock_run:
        main()
        mock_run.assert_called_once()


def test_main_entry():
    with patch("main.mcp.run") as mock_run:
        main_entry.main()
        mock_run.assert_called_once()
