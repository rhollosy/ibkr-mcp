---
name: ibkr
description: Manage Interactive Brokers (IBKR) accounts, monitor portfolios, and execute trades. Use when you need to check balances, search for symbols, get market data snapshots, or place/manage orders via the IBKR Client Portal API.
---

# IBKR Skill

## Overview

This skill provides a high-level interface for interacting with the Interactive Brokers Client Portal API. It allows you to check account statuses, search for financial instruments, monitor your portfolio, and manage orders.

## Quick Start

1. **Check Connectivity**: Always start by checking the authentication status.
   - Use `get_auth_status()` to ensure the Gateway is connected and the session is active.
2. **Identify Accounts**: List available accounts to get the `accountId`.
   - Use `get_accounts()`.
3. **Search for Instruments**: Find the `conid` (Contract ID) for the symbol you want to trade.
   - Use `search_contract(symbol="AAPL")`.

## Core Tasks

### 1. Account & Portfolio Monitoring
- **Balances**: Use `get_account_summary(account_id="U1234567")` for detailed equity and margin info.
- **Positions**: Use `get_positions(account_id="U1234567")` to see current holdings.
- **Open Orders**: Use `get_open_orders()` to see active, unfilled orders.

### 2. Market Data
- **Price Snapshots**: After finding a `conid`, use `get_market_data(conid=265598)` to get the last price, bid, and ask.
- **Symbol Search**: Always verify the `conid` and `exchange` using `search_contract()`.

### 3. Trading & Order Management
- **Place Order**: 
  - Required: `account_id`, `conid`, `side` (BUY/SELL), `quantity`, `order_type` (MKT/LMT).
  - Optional: `price` (for LMT orders).
  - Tool: `place_order(account_id="U1234567", conid=265598, side="BUY", quantity=10, order_type="MKT")`.
- **Modify Order**: Change quantity or price of an active order using `modify_order()`.
- **Cancel Order**: Use `cancel_order(account_id="U1234567", order_id="12345678")`.

## Important Considerations

- **Gateway Dependency**: This skill requires the IBKR Client Portal Gateway to be running locally (usually on port 5001).
- **Duplicate Orders**: The `place_order` tool includes logic to warn about potential duplicate orders. Pay attention to warnings in the response.
- **Conids**: Always use `search_contract` to find the correct `conid` for an instrument. Symbols can be ambiguous across different exchanges.
- **Safety**: Double-check the `side` and `quantity` before executing `place_order`.

## Examples

### Scenario: Checking AAPL Position and Placing a Limit Order
1. `get_auth_status()` -> Confirmed authenticated.
2. `get_accounts()` -> Found account `U1234567`.
3. `get_positions(account_id="U1234567")` -> No AAPL found.
4. `search_contract(symbol="AAPL")` -> Found `conid: 265598`.
5. `get_market_data(conid=265598)` -> Last price is $180.25.
6. `place_order(account_id="U1234567", conid=265598, side="BUY", quantity=5, order_type="LMT", price=180.00)`.
