# ibkr-mcp

MCP server for Interactive Brokers Web API (Client Portal API).

> [!IMPORTANT]
> **DISCLAIMER**: Trading financial instruments involves significant risk and can result in the loss of all your capital. This software is provided "as is" without warranty of any kind. Use of this software is at your own risk and peril. The author(s) and contributors are not responsible for any financial losses, technical errors, or other damages resulting from the use of this software. Always test in a paper trading environment before using with real capital.

## Features
- **Connection Check**: Verify Gateway status and session auth.
- **Account Discovery**: List available accounts and summaries.
- **Portfolio Monitoring**: View real-time positions.
- **Market Data**: Search contracts and get price snapshots.
- **Order Management**: Place, modify, and cancel orders.
- **Duplicate Detection**: Native warning bubbling for duplicate orders.
- **Latency Monitoring**: Automatic warnings for slow gateway responses.

## Setup & Running

### Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv)
- [IBKR Client Portal API Gateway](https://www.interactivebrokers.com/en/trading/ibkr-api.php)

### 1. Setup the IBKR Gateway
Follow the instructions in [docs/setup.md](docs/setup.md) to install and configure the IBKR Client Portal Gateway. Note that the Gateway URL is configurable via environment variables.

### 2. Environment Variables
The server requires the following variables:
- `IBKR_GATEWAY_URL`: e.g., `https://localhost:5001/v1/api`
- `IBKR_GATEWAY_VERIFY_SSL`: `false` (recommended for local dev with self-signed certs)

### 3. Install Dependencies
```bash
uv sync
```

### 4. Run the Server
#### Local Development
```bash
export IBKR_GATEWAY_URL="https://localhost:5001/v1/api"
export IBKR_GATEWAY_VERIFY_SSL="false"
uv run src/main.py
```

#### Remote Execution (via uvx)
You can also run the server directly from the remote repository without cloning:
```bash
export IBKR_GATEWAY_URL="https://localhost:5001/v1/api"
export IBKR_GATEWAY_VERIFY_SSL="false"
uvx --from git+https://github.com/rhollosy/ibkr-mcp ibkr-mcp
```

#### Container (Docker / OCI)

A minimal, security-hardened image is available via the included `Dockerfile`.
The image runs as a **non-root user** and contains only the runtime artefacts.

**Build locally:**
```bash
docker build -t ibkr-mcp .
```

**Run:**
```bash
docker run --rm -i \
  -e IBKR_GATEWAY_URL="https://host.docker.internal:5001/v1/api" \
  -e IBKR_GATEWAY_VERIFY_SSL="false" \
  ibkr-mcp
```

> [!NOTE]
> The server uses **stdio** transport (stdin/stdout). Pass `-i` (interactive) so
> the MCP host can write to the container's stdin. On Linux replace
> `host.docker.internal` with your host IP or `--network=host`.

**Configure an AI agent to use the container** (example for Claude Desktop / Gemini):
```json
{
  "mcpServers": {
    "ibkr": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-e", "IBKR_GATEWAY_URL=https://host.docker.internal:5001/v1/api",
        "-e", "IBKR_GATEWAY_VERIFY_SSL=false",
        "ibkr-mcp"
      ]
    }
  }
}
```

## AI Agent Integration
For detailed instructions on how to configure this server with AI agents like Gemini or Claude Desktop, see the [Setup & Integration Guide](docs/setup.md).

## Available Tools

- `get_auth_status()`: Checks Gateway connection and session.
- `get_accounts()`: Lists all accounts.
- `get_account_summary(account_id)`: Detailed balances.
- `get_positions(account_id)`: Active portfolio holdings.
- `search_contract(symbol)`: Look up conids.
- `get_market_data(conid)`: Current price snapshot.
- `place_order(...)`: Submit new orders.
- `modify_order(...)`: Adjust active orders.
- `cancel_order(...)`: Cancel active orders.
- `get_open_orders()`: List active orders.

## Development

### Testing
```bash
uv run pytest --cov=src
```

### Performance Check
```bash
uv run python scripts/perf-check.py
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
