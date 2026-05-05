# Data Model: ibkr-web-api-mcp

## Entities

### Account
Represents the user's trading account.
- `id` (string): The IBKR account ID (e.g., "U1234567").
- `type` (string): Account type (INDIVIDUAL, JOINT, etc.).
- `currency` (string): Base currency.
- `summary` (object): Balances like NetLiquidation, EquityWithLoanValue, AvailableFunds.

### Position
A holding within an account.
- `conid` (integer): Unique contract ID.
- `symbol` (string): Asset symbol (e.g., "AAPL").
- `size` (number): Number of shares or contracts.
- `avg_price` (number): Average cost basis.
- `market_value` (number): Current market value.

### Contract
A tradable instrument.
- `conid` (integer): Unique contract ID.
- `symbol` (string): Asset symbol.
- `asset_class` (string): STK, OPT, FUT, etc.
- `exchange` (string): Primary exchange.
- `details` (object): Additional info (expiry, strike for options).

### Order
An order request or active order.
- `id` (string): IBKR internal order ID.
- `conid` (integer): Target contract ID.
- `side` (string): BUY, SELL.
- `order_type` (string): LMT, MKT, STP.
- `quantity` (number): Total amount.
- `status` (string): Submitted, Pending, Filled, Cancelled.

#### Supported Modifications
- `quantity` (number): Update total amount.
- `price` (number): Update limit/stop price.
- `order_type` (string): Change between LMT, MKT, STP.
- `tif` (string): Update Time-In-Force (GTC, DAY).

## State Transitions (Orders)
- `Pending` → `Submitted` (sent to exchange)
- `Submitted` → `Filled` (execution)
- `Submitted` → `Cancelled` (user or system action)
