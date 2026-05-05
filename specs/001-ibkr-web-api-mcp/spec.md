# Feature Specification: ibkr-web-api-mcp

**Feature Branch**: `001-ibkr-web-api-mcp`  
**Created**: 2026-04-30  
**Status**: Draft  
**Input**: User description: "build a MCP server which will make use of Interactive Brokers WEB API. Link to the reference at `https://www.interactivebrokers.com/campus/ibkr-api-page/webapi-ref/`, documentation at `https://www.interactivebrokers.com/campus/ibkr-api-page/web-api/`."

## Clarifications

### Session 2026-04-30
- Q: How should the MCP server handle sensitive information like Account IDs in tool outputs and internal logs? → A: Show full account IDs in tool outputs; do not mask in logs.
- Q: Should the "modify order" tool support all IBKR-allowed modifications, or focus on common adjustments (price and quantity)? → A: Support all IBKR-allowed modifications (price, quantity, order type, etc.).
- Q: How should the MCP server react if the gateway is running but the session is not authenticated (requires user 2FA login)? → A: Return an informative message with the Gateway URL and a login instruction.
- Q: What should the MCP server do if an IBKR API request exceeds the 2-second target (e.g., due to gateway latency)? → A: Return the data with a warning if the request was slow.
- Q: How should the MCP server handle "potentially duplicate" orders (e.g., the same quantity and price submitted twice within a short window)? → A: Bubble up the Gateway's native duplicate detection warning to the user.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Connect and Authenticate (Priority: P1)

The MCP server needs to connect to the IBKR Client Portal API Gateway. To ensure ease of use, the server provides clear documentation to set up and launch the gateway.

**Why this priority**: Without authentication and a running gateway, none of the other features will work.

**Independent Test**: Can be fully tested by successfully validating the authentication status endpoint once the gateway is running.

**Acceptance Scenarios**:
1. **Given** the gateway is running but unauthenticated, **When** the server checks status, **Then** it prompts the user to log in via the web browser.
2. **Given** an authenticated gateway, **When** the server calls the auth status endpoint, **Then** it receives a confirmed authentication response.

---

### User Story 2 - Account & Portfolio Info (Priority: P1)

Users want to use the MCP tools to quickly check their account balances and view current portfolio positions.

**Why this priority**: Read-only information is the most common use case and presents no financial risk, making it an ideal first milestone.

**Independent Test**: Can be tested by invoking the account summary and portfolio tools and verifying the returned JSON structure.

**Acceptance Scenarios**:
1. **Given** an authenticated session, **When** the client calls the `get_account_summary` tool, **Then** the server returns account balances (e.g., NetLiquidation, AvailableFunds).
2. **Given** an authenticated session, **When** the client calls the `get_portfolio_positions` tool, **Then** the server returns a list of current holdings.

---

### User Story 3 - Market Data & Contract Search (Priority: P2)

Users want to look up contracts (stocks, options, futures) and get market data quotes before making trading decisions.

**Why this priority**: Contract IDs (conids) are required for placing orders, and market data is needed for pricing.

**Independent Test**: Can be tested by searching for a common symbol (e.g., "AAPL") and verifying the returned contract IDs and subsequent market data snapshots.

**Acceptance Scenarios**:
1. **Given** an authenticated session, **When** the client searches for symbol "MSFT", **Then** the server returns the matching contract details.
2. **Given** a valid contract ID, **When** the client requests market data, **Then** the server returns the latest bid, ask, and last prices.

---

### User Story 4 - Order Management (Priority: P2)

Users want to place new orders, view active orders, and cancel orders directly through the MCP interface.

**Why this priority**: Provides the full write-access capabilities requested by the user, enabling automated or AI-driven trading.

**Independent Test**: Can be tested in a paper-trading account by placing an order, verifying its status in the open orders list, and canceling it.

**Acceptance Scenarios**:
1. **Given** an authenticated paper-trading session, **When** the client submits a valid buy order, **Then** the order is accepted and an order ID is returned.
2. **Given** an active order, **When** the client requests the open orders list, **Then** the new order is included.
3. **Given** an active order, **When** the client submits a cancellation request, **Then** the order is canceled.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide documentation enabling a new user to start the local gateway and connect the MCP server in under 10 minutes.
- **FR-002**: System MUST expose an MCP tool to check the gateway's authentication status (`/iserver/auth/status`).
- **FR-003**: System MUST expose an MCP tool to retrieve account summaries (`/portfolio/accounts` and `/portfolio/{accountId}/summary`).
- **FR-004**: System MUST expose an MCP tool to list portfolio positions (`/portfolio/{accountId}/positions`).
- **FR-005**: System MUST expose an MCP tool to search for contracts by symbol (`/iserver/secdef/search`).
- **FR-006**: System MUST expose an MCP tool to request market data snapshots (`/iserver/marketdata/snapshot`).
- **FR-007**: System MUST expose MCP tools to place, modify (full range), and cancel orders (`/iserver/account/{accountId}/orders`, etc.).
- **FR-008**: System MUST gracefully handle gateway timeout and authentication errors, returning clear, actionable instructions (including the Gateway URL) for user login to the MCP client.
- **FR-009**: System MUST detect and bubble up the Gateway's native duplicate order warnings/errors to the MCP client to prevent accidental double-execution.

### Key Entities

- **Account**: Represents the user's IBKR account, containing ID, balances, and margin info.
- **Position**: A holding in the portfolio (e.g., 100 shares of AAPL).
- **Contract**: A tradable instrument defined by its `conid` (contract ID), symbol, and asset class.
- **Order**: A request to buy or sell a contract, tracking status (submitted, filled, canceled).

## Edge Cases

- **Authentication Lapse**: If the gateway session expires, the server MUST return a structured error with the Gateway login URL.
- **Gateway Timeout**: Requests exceeding 2 seconds trigger a "Slow Response" warning header in the tool output.
- **Duplicate Orders**: Native IBKR duplicate detection warnings (e.g., same price/size) must be bubbled up as actionable warnings, not silent failures.
- **Network Connectivity**: Loss of connection to the local gateway should be reported as a `GatewayTimeoutError`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The MCP server successfully connects to and queries the IBKR Gateway running locally.
- **SC-002**: Users can retrieve a valid portfolio summary containing current positions within 2 seconds of tool invocation; the server MUST append a warning to the output of ANY tool if the Gateway response exceeds this 2-second target.
- **SC-003**: The server correctly resolves a common stock symbol (e.g., TSLA) to its primary `conid`.
- **SC-004**: Users can successfully place and cancel a paper trading order via the MCP tools.
- **SC-005**: The server exposes all functional requirements as distinct, callable MCP tools.

## Assumptions

- Users have an existing IBKR account (paper or live) and have enabled Client Portal API access.
- Users are capable of running the IBKR Client Portal API Gateway locally (requires Java/Node or Docker).
- Trading operations will be tested primarily in paper-trading mode to prevent accidental financial loss.
- The server will communicate with the local gateway over HTTP/HTTPS as defined in the standard IBKR documentation.
