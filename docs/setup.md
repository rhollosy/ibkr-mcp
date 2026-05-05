# IBKR Client Portal Gateway: Setup & Integration Guide

This document outlines the requirements, installation, and AI agent integration process for the IBKR MCP server.

## 1. Prerequisites

### System Requirements
- **Account**: IBKR PRO account (Lite accounts are not supported).
- **Java**: Java Runtime Environment (JRE) 8 update 192 or higher.
- **Python**: 3.11+
- **Package Manager**: [uv](https://github.com/astral-sh/uv) (recommended).
- **Connectivity**: The gateway MUST run on the same machine where the API commands are generated.

### Authentication & Sessions
- **Manual 2FA**: Automated login is NOT supported. You must manually log in via a browser.
- **Session Types**: 
  - **Read-Only**: Created on initial login.
  - **Brokerage**: Required for trading/market data (requires explicit 2FA).
- **Persistence**: Sessions reset daily at midnight (local time).

## 2. Gateway Installation & Configuration

### Standalone Installation
1. Download the Gateway (Standard or Beta) from the [IBKR website](https://www.interactivebrokers.com/en/trading/ibkr-api.php).
2. Unzip the package to a local directory.
3. **macOS Note**: Port `5000` is often used by AirPlay Receiver. It is recommended to change the `listenPort` to `5001` in `root/conf.yaml`.

### Configuration (`root/conf.yaml`)
Ensure your `conf.yaml` includes:
```yaml
listenPort: 5001
proxyRemoteHost: https://api.ibkr.com
listenSsl: true
```

### Running the Gateway
- **Standalone**: `bin/run.sh root/conf.yaml` (Unix) or `bin\run.bat root\conf.yaml` (Windows).
- **Docker**: `docker run -p 5001:5001 -e "GW_PORT=5001" interactivebrokers/cp-gateway`

## 3. MCP Server Configuration

The MCP server relies on these environment variables to connect to the Gateway:

| Variable | Description | Example |
|----------|-------------|---------|
| `IBKR_GATEWAY_URL` | The full base URL for the Gateway API. | `https://localhost:5001/v1/api` |
| `IBKR_GATEWAY_VERIFY_SSL` | Set to `false` if using self-signed certs. | `false` |

## 4. AI Agent Integration

### Gemini CLI
Add this to your `.gemini/settings.json`:

**Option A: Local Clone**
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

**Option B: Remote Execution (uvx)**
```json
{
  "mcpServers": {
    "ibkr": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/rhollosy/ibkr-mcp", "ibkr-mcp"],
      "env": {
        "IBKR_GATEWAY_URL": "https://localhost:5001/v1/api",
        "IBKR_GATEWAY_VERIFY_SSL": "false"
      }
    }
  }
}
```

### Claude Desktop
Add to `claude_desktop_config.json` (macOS: `~/Library/Application Support/Claude/`):

**Option A: Local Clone**
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

**Option B: Remote Execution (uvx)**
```json
{
  "mcpServers": {
    "ibkr": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/rhollosy/ibkr-mcp", "ibkr-mcp"],
      "env": {
        "IBKR_GATEWAY_URL": "https://localhost:5001/v1/api",
        "IBKR_GATEWAY_VERIFY_SSL": "false"
      }
    }
  }
}
```

## 5. Usage & Maintenance

### Session Maintenance (Tickle)
The gateway requires a heartbeat every 5 minutes. The MCP server's `get_auth_status` tool handles this, or you can use:
`curl -k -X GET "https://localhost:5001/v1/api/tickle"`

### Troubleshooting
- **Connection Refused**: Ensure the Gateway is running on the correct port.
- **Authentication Error**: Visit `https://localhost:5001` in your browser to re-authenticate (2FA).
- **SSL Errors**: Set `IBKR_GATEWAY_VERIFY_SSL=false` if encountering certificate issues.
