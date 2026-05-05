# Quickstart: ibkr-web-api-mcp

## Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- IBKR Client Portal API Gateway (Java/Node versions supported)
- An active IBKR Account (Paper trading recommended for initial setup)

## Setup
1. **Launch IBKR Gateway**: Follow [docs/setup.md](../../docs/setup.md) to install and start the gateway.
2. **Login**: Perform the manual 2FA login via the Gateway URL (e.g., `https://localhost:5001`).
3. **Environment Setup**:
   ```bash
   uv sync
   ```
4. **Run Server**:
   **Option A: Local Clone**
   ```bash
   export IBKR_GATEWAY_URL="https://localhost:5001/v1/api"
   export IBKR_GATEWAY_VERIFY_SSL="false"
   uv run src/main.py
   ```

   **Option B: Remote Execution (uvx)**
   ```bash
   export IBKR_GATEWAY_URL="https://localhost:5001/v1/api"
   export IBKR_GATEWAY_VERIFY_SSL="false"
   uvx --from git+https://github.com/rhollosy/ibkr-mcp ibkr-mcp
   ```

## Development & Testing
- **Run Tests**: `uv run pytest --cov=src`
- **Linting**: `uv run ruff check .`
