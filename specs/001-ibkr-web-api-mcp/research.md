# Technical Context Research: ibkr-web-api-mcp

## 1. FastMCP Framework
**Decision**: Use `FastMCP` (Python-based) for the server implementation.
**Rationale**: FastMCP provides a high-level, decorator-based API for defining tools and resources, aligning with Constitution Principle III. It simplifies server initialization and tool registration.
**Alternatives considered**: standard `mcp` Python SDK (more boilerplate, lower-level).

## 2. Asynchronous API Communication
**Decision**: Use `httpx` as the asynchronous HTTP client.
**Rationale**: Constitution requires all external API calls to be asynchronous. `httpx` is the industry standard for async Python HTTP requests and integrates perfectly with `FastMCP`'s async nature.
**Implementation**: Use `httpx.AsyncClient` with connection pooling to minimize latency to the local gateway.

## 3. IBKR Gateway Session Management
**Decision**: The MCP server will perform a heartbeat check via `/iserver/auth/status` and report authentication state.
**Rationale**: IBKR API sessions expire and require manual 2FA. Automating this is forbidden by Constitution Principle IV.
**Failure Mode**: If unauthenticated, the server will return the Gateway URL as clarified in Session 2026-04-30.

## 4. Test Coverage (>= 90%)
**Decision**: Use `pytest` with `pytest-cov` and `pytest-asyncio`.
**Rationale**: Necessary to satisfy Constitution Principle II. Robust mocking of the Gateway responses will be required to achieve 90% coverage without a live account connection during CI.

## 5. Modern Python Tooling (uv)
**Decision**: Use `uv` for dependency and virtual environment management.
**Rationale**: Adheres to Constitution Principle V for deterministic and high-performance development environments.
