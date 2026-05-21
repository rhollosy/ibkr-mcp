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
- **Order Confirmations**: Native handling of Gateway confirmation dialogs.
- **Duplicate Detection**: Native warning bubbling for duplicate orders.
- **Latency Monitoring**: Automatic warnings for slow gateway responses.
- **Session Keepalive**: Background heartbeat keeps the Gateway session alive.

## Setup & Running

### Prerequisites

- [IBKR Client Portal API Gateway](https://www.interactivebrokers.com/en/trading/ibkr-api.php) running locally
- See [docs/setup.md](docs/setup.md) for full Gateway installation & configuration

### Environment Variables

| Variable | Description | Example |
|---|---|---|
| `IBKR_GATEWAY_URL` | Full base URL of the Gateway API | `https://localhost:5001/v1/api` |
| `IBKR_GATEWAY_VERIFY_SSL` | Disable SSL verification for self-signed certs | `false` |

### Running the MCP Server

Choose the deployment method that suits your workflow. All options expose identical MCP tools over **stdio** transport.

---

#### Option A — `uvx` (no install required)

Runs the server directly from the remote repository. Requires [uv](https://github.com/astral-sh/uv).

```bash
uvx --from git+https://github.com/rhollosy/ibkr-mcp ibkr-mcp \
  --env IBKR_GATEWAY_URL="https://localhost:5001/v1/api" \
  --env IBKR_GATEWAY_VERIFY_SSL="false"
```

---

#### Option B — Docker (no Python required)

A minimal, security-hardened OCI image. Runs as a non-root user. No Python or uv installation needed on the host.

```bash
# Build once
docker build -t ibkr-mcp https://github.com/rhollosy/ibkr-mcp.git

# Run
docker run --rm -i \
  -e IBKR_GATEWAY_URL="https://host.docker.internal:5001/v1/api" \
  -e IBKR_GATEWAY_VERIFY_SSL="false" \
  ibkr-mcp
```

> [!NOTE]
> Pass `-i` (interactive) so the MCP host can write to stdin. On Linux replace
> `host.docker.internal` with your host IP or use `--network=host`.

---

#### Option C — Local Clone (development)

```bash
git clone https://github.com/rhollosy/ibkr-mcp
cd ibkr-mcp
uv sync
export IBKR_GATEWAY_URL="https://localhost:5001/v1/api"
export IBKR_GATEWAY_VERIFY_SSL="false"
uv run src/main.py
```

---

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

For detailed per-agent configuration (Gemini CLI, Claude Desktop, VS Code) covering all three deployment methods, see the **[Setup & Integration Guide](docs/setup.md)**.

## Available Tools

| Tool | Description |
|---|---|
| `get_auth_status()` | Check Gateway connection and session |
| `get_accounts()` | List all accounts |
| `get_account_summary(account_id)` | Detailed balances |
| `get_positions(account_id)` | Active portfolio holdings |
| `search_contract(symbol)` | Look up contract IDs (conids) |
| `get_market_data(conid)` | Current price snapshot |
| `place_order(...)` | Submit new orders |
| `reply_to_confirmation(reply_id, confirmed)` | Confirm interactive order dialogs |
| `modify_order(...)` | Adjust active orders |
| `cancel_order(...)` | Cancel active orders |
| `get_open_orders()` | List active orders |

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
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
