import logging
import os
import re
from typing import Any

import httpx

from .exceptions import (
    AuthenticationError,
    GatewayTimeoutError,
    InvalidInputError,
    RequestError,
)
from .models import Account, Contract, MarketDataSnapshot, Order, Position

logger = logging.getLogger(__name__)

# Account, order and reply IDs are interpolated into URL paths, so restrict them
# to characters that cannot change the path (no "/", "..", "?" or "#").
_PATH_ID_RE = re.compile(r"[A-Za-z0-9_-]+")


def _path_id(name: str, value: str) -> str:
    value = str(value)
    if not _PATH_ID_RE.fullmatch(value):
        raise InvalidInputError(f"Invalid {name}: {value!r}")
    return value


class IBKRClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        # IBKR Gateway uses self-signed certs by default in local dev.
        # Allow disabling verification via env var, but default to True for security.
        verify_ssl = os.getenv("IBKR_GATEWAY_VERIFY_SSL", "true").lower() == "true"

        # T007: Implement connection pooling (max_connections: 10, keepalive: 5s)
        limits = httpx.Limits(
            max_connections=10, max_keepalive_connections=10, keepalive_expiry=5.0
        )
        self.client = httpx.AsyncClient(
            base_url=base_url, verify=verify_ssl, limits=limits, timeout=10.0
        )

    async def _request(self, method: str, path: str, **kwargs) -> Any:
        try:
            response = await self.client.request(method, path, **kwargs)
            response.raise_for_status()
            if not response.content:
                return {}
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise AuthenticationError(
                    "Gateway session expired or unauthenticated"
                ) from e
            raise RequestError(f"API request failed: {e}") from e
        except httpx.ConnectError as e:
            raise GatewayTimeoutError(
                "Could not connect to IBKR Gateway. Is it running?"
            ) from e
        except httpx.TimeoutException as e:
            raise GatewayTimeoutError("IBKR Gateway did not respond in time") from e
        except httpx.TransportError as e:
            raise RequestError(f"API request failed: {e}") from e
        except ValueError as e:
            raise RequestError(f"Gateway returned an invalid JSON response: {e}") from e

    async def get_auth_status(self) -> dict[str, Any]:
        """Check authentication status."""
        return await self._request("POST", "/iserver/auth/status")

    async def tickle(self) -> dict[str, Any]:
        """Ping the server to keep the session open."""
        return await self._request("POST", "/tickle")

    async def get_accounts(self) -> list[Account]:
        """List all accounts."""
        raw_accounts = await self._request("GET", "/portfolio/accounts")
        return [Account.model_validate(a) for a in raw_accounts]

    async def get_account_summary(self, account_id: str) -> dict[str, Any]:
        """Get summary for a specific account."""
        account_id = _path_id("account_id", account_id)
        return await self._request("GET", f"/portfolio/{account_id}/summary")

    async def get_positions(self, account_id: str) -> list[Position]:
        """Get positions for a specific account."""
        account_id = _path_id("account_id", account_id)
        raw_positions = await self._request("GET", f"/portfolio/{account_id}/positions")
        return [Position.model_validate(p) for p in raw_positions]

    async def search_contract(self, symbol: str) -> list[Contract]:
        """Search for a contract by symbol."""
        payload = {"symbol": symbol}
        raw_contracts = await self._request(
            "POST", "/iserver/secdef/search", json=payload
        )
        return [Contract.model_validate(c) for c in raw_contracts]

    async def get_market_data(self, conids: list[int]) -> list[MarketDataSnapshot]:
        """Get market data snapshot for contract IDs."""
        conid_str = ",".join(map(str, conids))
        params = {"conids": conid_str, "fields": "31,84,86,82"}
        raw_snapshots = await self._request(
            "GET", "/iserver/marketdata/snapshot", params=params
        )
        return [MarketDataSnapshot.model_validate(s) for s in raw_snapshots]

    async def place_orders(
        self, account_id: str, orders: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Place orders for a specific account."""
        account_id = _path_id("account_id", account_id)
        path = f"/iserver/account/{account_id}/orders"
        return await self._request("POST", path, json={"orders": orders})

    async def modify_order(
        self, account_id: str, order_id: str, order_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Modify an existing order."""
        account_id = _path_id("account_id", account_id)
        order_id = _path_id("order_id", order_id)
        path = f"/iserver/account/{account_id}/order/{order_id}"
        return await self._request("POST", path, json=order_data)

    async def cancel_order(self, account_id: str, order_id: str) -> dict[str, Any]:
        """Cancel an existing order."""
        account_id = _path_id("account_id", account_id)
        order_id = _path_id("order_id", order_id)
        path = f"/iserver/account/{account_id}/order/{order_id}"
        return await self._request("DELETE", path)

    async def get_open_orders(self) -> dict[str, Any]:
        """Get all open orders."""
        raw_data = await self._request("GET", "/iserver/account/orders")
        orders = raw_data.get("orders", [])
        raw_data["orders"] = [Order.model_validate(o) for o in orders]
        return raw_data

    async def reply_to_confirmation(
        self, reply_id: str, confirmed: bool
    ) -> list[dict[str, Any]]:
        """Reply to a Gateway-issued order confirmation question."""
        reply_id = _path_id("reply_id", reply_id)
        path = f"/iserver/reply/{reply_id}"
        return await self._request("POST", path, json={"confirmed": confirmed})

    async def close(self):
        await self.client.aclose()
