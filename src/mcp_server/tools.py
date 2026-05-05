
from .server import get_client, mcp
from .utils import catch_errors, warn_if_slow


@mcp.tool()
@catch_errors()
@warn_if_slow()
async def get_auth_status() -> str:
    """Check if the MCP server is connected to an authenticated IBKR Gateway session."""
    client = get_client()
    status = await client.get_auth_status()
    if status.get("authenticated"):
        return "Authenticated: Gateway is connected and session is active."
    
    # Derive the UI login URL from the base API URL (e.g., strip /v1/api)
    gateway_ui_url = client.base_url.replace("/v1/api", "")
    return (
        "Unauthenticated: Please log in via the IBKR Gateway UI.\n"
        f"Gateway URL: {gateway_ui_url}"
    )

@mcp.tool()
@catch_errors()
@warn_if_slow()
async def get_accounts() -> str:
    """List all accounts available to the user."""
    client = get_client()
    accounts = await client.get_accounts()
    if not accounts:
        return "No accounts found."
    lines = [
        f"- {a.get('accountId', 'Unknown')} ({a.get('accountName', 'N/A')})" 
        for a in accounts
    ]
    return "Accounts:\n" + "\n".join(lines)

@mcp.tool()
@catch_errors()
@warn_if_slow()
async def get_account_summary(account_id: str) -> str:
    """Get summary balances for a specific account."""
    client = get_client()
    summary = await client.get_account_summary(account_id)
    # Simplify the output for readability
    lines = [
        f"{k}: {v}" 
        for k, v in summary.items() 
        if isinstance(v, (int, float, str))
    ]
    return f"Summary for {account_id}:\n" + "\n".join(lines)

@mcp.tool()
@catch_errors()
@warn_if_slow()
async def get_positions(account_id: str) -> str:
    """List current portfolio positions for a specific account."""
    client = get_client()
    positions = await client.get_positions(account_id)
    if not positions:
        return f"No positions found for {account_id}."
    lines = []
    for p in positions:
        symbol = p.get("contractDesc") or p.get("symbol") or "Unknown"
        conid = p.get("conid", "N/A")
        pos = p.get("position", 0)
        avg = p.get("avgPrice", 0)
        mkt = p.get("mktPrice", 0)
        lines.append(f"- {symbol} ({conid}): {pos} @ {avg} (Mkt: {mkt})")
    return f"Positions for {account_id}:\n" + "\n".join(lines)

@mcp.tool()
@catch_errors()
@warn_if_slow()
async def search_contract(symbol: str) -> str:
    """Search for a contract by symbol."""
    client = get_client()
    results = await client.search_contract(symbol)
    if not results:
        return f"No contracts found for {symbol}."
    lines = [
        f"- {r.get('symbol', 'N/A')} ({r['conid']}): {r['assetClass']} @ {r.get('exchange', 'N/A')}"
        for r in results
    ]
    return f"Results for {symbol}:\n" + "\n".join(lines)

@mcp.tool()
@catch_errors()
@warn_if_slow()
async def get_market_data(conid: int) -> str:
    """Get market data snapshot for a specific contract ID (conid)."""
    client = get_client()
    data = await client.get_market_data([conid])
    if not data:
        return f"No market data found for {conid}."
    d = data[0]
    # Map fields: 31=Last, 84=Bid, 86=Ask, 82=Change
    return (
        f"Snapshot for {conid}:\n"
        f"Last: {d.get('31', 'N/A')}\n"
        f"Bid: {d.get('84', 'N/A')}\n"
        f"Ask: {d.get('86', 'N/A')}\n"
        f"Change: {d.get('82', 'N/A')}"
    )

@mcp.tool()
@catch_errors()
@warn_if_slow()
async def place_order(
    account_id: str,
    conid: int,
    side: str,
    quantity: float,
    order_type: str,
    price: float | None = None
) -> str:
    """Place a new order."""
    client = get_client()
    order = {
        "conid": conid,
        "side": side,
        "quantity": quantity,
        "orderType": order_type,
    }
    if price:
        order["lmtPrice"] = price

    response = await client.place_orders(account_id, [order])
    # Handle duplicate warnings
    msg = f"Order Result: {response}"
    if (isinstance(response, list) and 
        len(response) > 0 and 
        "warning" in str(response[0]).lower()):
        msg = f"WARNING: Potential duplicate detected.\n{response}"
    return msg

@mcp.tool()
@catch_errors()
@warn_if_slow()
async def modify_order(
    account_id: str,
    order_id: str,
    quantity: float | None = None,
    price: float | None = None
) -> str:
    """Modify an existing order."""
    client = get_client()
    data = {}
    if quantity:
        data["quantity"] = quantity
    if price:
        data["lmtPrice"] = price
    
    response = await client.modify_order(account_id, order_id, data)
    return f"Modify Result: {response}"

@mcp.tool()
@catch_errors()
@warn_if_slow()
async def cancel_order(account_id: str, order_id: str) -> str:
    """Cancel an active order."""
    client = get_client()
    response = await client.cancel_order(account_id, order_id)
    return f"Cancel Result: {response}"

@mcp.tool()
@catch_errors()
@warn_if_slow()
async def get_open_orders() -> str:
    """List all open orders."""
    client = get_client()
    data = await client.get_open_orders()
    orders = data.get("orders", [])
    if not orders:
        return "No open orders found."
    lines = []
    for o in orders:
        oid = o.get("orderId", "N/A")
        side = o.get("side", "N/A")
        rem = o.get("remainingQuantity", 0)
        total = o.get("totalSize") or o.get("totalQuantity") or 0
        symbol = o.get("ticker") or o.get("symbol") or "Unknown"
        price = o.get("lmtPrice") or o.get("auxPrice") or "MKT"
        status = o.get("status", "Unknown")
        lines.append(f"- {oid}: {side} {rem}/{total} {symbol} @ {price} ({status})")
    return "Open Orders:\n" + "\n".join(lines)
