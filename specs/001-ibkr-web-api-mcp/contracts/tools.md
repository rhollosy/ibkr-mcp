# MCP Tool Contracts: ibkr-web-api-mcp

## Tools Exposed

### `get_auth_status`
- **Purpose**: Check if the MCP server is connected to an authenticated IBKR Gateway session.
- **Output**: JSON containing `authenticated` (bool), `username` (string), and `message` (string).

### `get_accounts`
- **Purpose**: List all accounts available to the user.
- **Output**: Array of `Account` objects.

### `get_account_summary`
- **Input**: `accountId` (string)
- **Output**: Summary balances for the specified account.

### `get_positions`
- **Input**: `accountId` (string)
- **Output**: Array of `Position` objects.

### `search_contract`
- **Input**: `symbol` (string), `assetClass` (optional string)
- **Output**: Array of matching `Contract` objects.

### `get_market_data`
- **Input**: `conid` (integer)
- **Output**: Latest bid/ask/last prices and change info.

### `place_order`
- **Input**: `accountId`, `conid`, `side`, `quantity`, `orderType`, `price` (optional)
- **Output**: Order confirmation or error message.

### `modify_order`
- **Input**: `accountId`, `orderId`, `quantity` (optional), `price` (optional), `orderType` (optional), `tif` (optional), `outsideRth` (optional)
- **Output**: Success confirmation or error message.

### `cancel_order`
- **Input**: `accountId`, `orderId`
- **Output**: Success confirmation or error message.
