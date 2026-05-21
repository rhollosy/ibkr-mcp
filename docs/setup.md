# IBKR Client Portal Gateway — Setup & Integration Guide

This document covers Gateway installation, MCP server configuration, and AI agent integration. Every agent section shows **both** the `uvx` and `docker` deployment methods side-by-side.

---

## 1. Prerequisites

### System Requirements

| Requirement | Details |
|---|---|
| **IBKR Account** | PRO account (Lite accounts are not supported) |
| **Java** | JRE 8 update 192 or higher (for the Gateway) |
| **Python** | 3.11+ — only needed for the `uvx` / local-clone methods |
| **uv** | [astral-sh/uv](https://github.com/astral-sh/uv) — only needed for `uvx` / local-clone |
| **Docker** | Any OCI-compatible runtime — only needed for the Docker method |
| **Connectivity** | Gateway must run on the same machine that generates API commands |

### Authentication & Sessions

- **Manual 2FA**: Automated login is **not** supported. You must authenticate via a browser.
- **Session types**:
  - *Read-Only* — created on initial login.
  - *Brokerage* — required for trading and market data (requires explicit 2FA confirmation).
- **Session reset**: Sessions expire daily at midnight (local time). The MCP server includes a background keepalive that ticks every 3 minutes to prevent earlier timeouts.

---

## 2. Gateway Installation & Configuration

### Standalone Installation

1. Download the Gateway (Standard or Beta) from the [IBKR website](https://www.interactivebrokers.com/en/trading/ibkr-api.php).
2. Unzip the package to a local directory.
3. **macOS**: Port `5000` is often occupied by AirPlay Receiver — change `listenPort` to `5001` in `root/conf.yaml`.

### Configuration (`root/conf.yaml`)

```yaml
listenPort: 5001
proxyRemoteHost: https://api.ibkr.com
listenSsl: true
```

### Running the Gateway

| Platform | Command |
|---|---|
| macOS / Linux | `bin/run.sh root/conf.yaml` |
| Windows | `bin\run.bat root\conf.yaml` |
| Docker | `docker run -p 5001:5001 -e GW_PORT=5001 interactivebrokers/cp-gateway` |

After starting, open `https://localhost:5001` in your browser and complete the 2FA login.

---

## 3. MCP Server — Environment Variables

Both `uvx` and Docker accept these variables at runtime:

| Variable | Description | Example |
|---|---|---|
| `IBKR_GATEWAY_URL` | Full base URL of the Gateway API | `https://localhost:5001/v1/api` |
| `IBKR_GATEWAY_VERIFY_SSL` | `false` disables SSL verification for self-signed certs | `false` |

---

## 4. AI Agent Integration

### Choosing a Deployment Method

| | `uvx` | Docker |
|---|---|---|
| **Requires Python** | Yes (via uv) | No |
| **Requires Docker** | No | Yes |
| **Isolation** | uv venv | Container (non-root) |
| **Auto-updates** | On each run from `main` | Only when image is rebuilt |
| **Footprint** | ~50 MB venv | ~200 MB image |

Pick the method that fits your environment and use the matching config snippet below.

---

### Gemini CLI

Edit `.gemini/settings.json` in your home directory or project root.

**Option A — uvx**
```json
{
  "mcpServers": {
    "ibkr": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/rhollosy/ibkr-mcp",
        "ibkr-mcp"
      ],
      "env": {
        "IBKR_GATEWAY_URL": "https://localhost:5001/v1/api",
        "IBKR_GATEWAY_VERIFY_SSL": "false"
      }
    }
  }
}
```

**Option B — Docker**
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

> [!NOTE]
> Build the image first: `docker build -t ibkr-mcp https://github.com/rhollosy/ibkr-mcp.git`
> On Linux replace `host.docker.internal` with your host IP or add `--network=host`.

---

### Claude Desktop

Edit `claude_desktop_config.json`:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

**Option A — uvx**
```json
{
  "mcpServers": {
    "ibkr": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/rhollosy/ibkr-mcp",
        "ibkr-mcp"
      ],
      "env": {
        "IBKR_GATEWAY_URL": "https://localhost:5001/v1/api",
        "IBKR_GATEWAY_VERIFY_SSL": "false"
      }
    }
  }
}
```

**Option B — Docker**
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

---

### VS Code (GitHub Copilot / MCP extension)

Edit `.vscode/mcp.json` in your workspace:

**Option A — uvx**
```json
{
  "servers": {
    "ibkr": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/rhollosy/ibkr-mcp",
        "ibkr-mcp"
      ],
      "env": {
        "IBKR_GATEWAY_URL": "https://localhost:5001/v1/api",
        "IBKR_GATEWAY_VERIFY_SSL": "false"
      }
    }
  }
}
```

**Option B — Docker**
```json
{
  "servers": {
    "ibkr": {
      "type": "stdio",
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

---

### Local Clone (Development / Self-hosting)

Use this method when you want to modify the server or run from a local checkout.

```bash
git clone https://github.com/rhollosy/ibkr-mcp
cd ibkr-mcp
uv sync
```

Then reference the local path in your agent config:

```json
{
  "mcpServers": {
    "ibkr": {
      "command": "uv",
      "args": ["--directory", "/path/to/ibkr-mcp", "run", "src/main.py"],
      "env": {
        "IBKR_GATEWAY_URL": "https://localhost:5001/v1/api",
        "IBKR_GATEWAY_VERIFY_SSL": "false"
      }
    }
  }
}
```

---

## 5. Usage & Maintenance

### Session Maintenance

The MCP server runs a background keepalive that calls the Gateway tickle endpoint every **3 minutes**. If you need to trigger it manually:

```bash
curl -k -X GET "https://localhost:5001/v1/api/tickle"
```

### Order Confirmation Flow

Some orders (e.g. first-time contract or large size) trigger an interactive confirmation dialog from the Gateway. The `place_order` tool will return a `reply_id` in this case. Pass it to `reply_to_confirmation` to complete the order:

```
place_order(account_id="U1234567", conid=265598, side="BUY", quantity=1, order_type="MKT")
# → "CONFIRMATION REQUIRED (Reply ID: abc-123): ..."

reply_to_confirmation(reply_id="abc-123", confirmed=True)
# → "Order placed successfully"
```

### Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `Connection refused` | Gateway not running | Start `bin/run.sh root/conf.yaml` and check port 5001 |
| `Authentication Error` | Session expired | Visit `https://localhost:5001` and re-authenticate (2FA) |
| `SSL Error` | Self-signed cert | Set `IBKR_GATEWAY_VERIFY_SSL=false` |
| Docker: `host not found` | Wrong host ref on Linux | Replace `host.docker.internal` with host IP or use `--network=host` |
| `IBKR_GATEWAY_URL not set` | Missing env var | Pass `-e IBKR_GATEWAY_URL=...` to `docker run` or add to `env` block |
