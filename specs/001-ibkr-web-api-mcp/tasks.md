# Tasks: ibkr-web-api-mcp

**Input**: Design documents from `specs/001-ibkr-web-api-mcp/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test tasks are included as 90% coverage is a core requirement (TDD approach per Constitution Principle II).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and environment configuration

- [X] T001 Initialize Python project using uv in repository root
- [X] T002 [P] Configure pyproject.toml with dependencies (fastmcp, httpx, pydantic) and dev dependencies (pytest, pytest-cov, pytest-asyncio, ruff)
- [X] T003 Create directory structure: src/ibkr, src/mcp_server, tests/unit, tests/integration
- [X] T004 [P] Configure ruff linting and pytest-cov (set --cov-fail-under=90) in pyproject.toml

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Implement custom exceptions (AuthenticationError, GatewayTimeoutError, RequestError) in src/ibkr/exceptions.py
- [X] T006 [P] Create Pydantic base models for IBKR payloads in src/ibkr/models.py
- [X] T007 Implement async IBKRClient base class with connection pooling (max_connections: 10, keepalive: 5s) in src/ibkr/client.py
- [X] T008 Initialize FastMCP server instance in src/mcp_server/server.py
- [X] T009 Implement heartbeat/auth-status check method in src/ibkr/client.py
- [X] T009b [P] [FR-008] Implement global error handling/middleware for all MCP tools to catch gateway timeouts and auth lapses in src/mcp_server/utils.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Connect and Authenticate (Priority: P1) 🎯 MVP

**Goal**: Establish verified connection to IBKR Gateway and report status.

**Independent Test**: Successfully invoke get_auth_status tool and receive clear state/instructions.

### Tests for User Story 1 ⚠️

- [X] T010 [P] [US1] Unit test for get_auth_status client method in tests/unit/test_ibkr_client.py
- [X] T011 [P] [US1] Integration test for get_auth_status tool in tests/integration/test_auth_tools.py

### Implementation for User Story 1

- [X] T012 [US1] Implement get_auth_status tool with actionable login instructions (Gateway URL) in src/mcp_server/tools.py
- [X] T013 [US1] Finalize US1 documentation in docs/setup.md

**Checkpoint**: User Story 1 functional - connection verified and instructions provided if unauthenticated.

---

## Phase 4: User Story 2 - Account & Portfolio Info (Priority: P1)

**Goal**: Retrieve account balances and current portfolio holdings.

**Independent Test**: Tools return valid account summary and position list JSON/text.

### Implementation for User Story 2

- [X] T016 [P] [US2] Define Account and Position Pydantic models in src/ibkr/models.py
- [X] T017 [US2] Implement account and portfolio retrieval methods in src/ibkr/client.py
- [X] T018 [US2] Implement get_accounts, get_account_summary, and get_portfolio_positions tools in src/mcp_server/tools.py

### Tests for User Story 2 ⚠️

- [X] T014 [P] [US2] Unit tests for portfolio and account summary client methods in tests/unit/test_ibkr_client.py
- [X] T015 [P] [US2] Integration tests for get_accounts, get_account_summary, and get_portfolio_positions tools in tests/integration/test_account_tools.py

**Checkpoint**: User Story 2 functional - Portfolio and account discovery complete.

---

## Phase 5: User Story 3 - Market Data & Contract Search (Priority: P2)

**Goal**: Find contract IDs and get real-time price snapshots.

**Independent Test**: Search resolves symbol to conid and snapshot tool returns price data.

### Implementation for User Story 3

- [X] T021 [P] [US3] Define Contract and MarketDataSnapshot Pydantic models in src/ibkr/models.py
- [X] T022 [US3] Implement search and market data snapshot methods in src/ibkr/client.py
- [X] T023 [US3] Implement search_contract and get_market_data tools in src/mcp_server/tools.py

### Tests for User Story 3 ⚠️

- [X] T019 [P] [US3] Unit test for contract search and market data client methods in tests/unit/test_ibkr_client.py
- [X] T020 [P] [US3] Integration test for search_contract and get_market_data tools in tests/integration/test_market_tools.py

**Checkpoint**: User Story 3 functional - Contract discovery and pricing enabled.

---

## Phase 6: User Story 4 - Order Management (Priority: P2)

**Goal**: Place, modify (full range), and cancel orders with duplicate detection.

**Independent Test**: Paper trade order cycle (submit -> list -> modify -> cancel) completes via MCP.

### Implementation for User Story 4

- [X] T026 [P] [US4] Define Order Pydantic model and lifecycle states in src/ibkr/models.py
- [X] T027 [US4] Implement order management methods (POST/DELETE/PUT) in src/ibkr/client.py
- [X] T028 [US4] Implement place_order, modify_order, cancel_order, and get_open_orders tools in src/mcp_server/tools.py
- [X] T029 [US4] Implement duplicate order warning bubbling logic from Gateway responses in src/ibkr/client.py

### Tests for User Story 4 ⚠️

- [X] T024 [P] [US4] Unit test for order submission, modification, and cancellation client methods in tests/unit/test_ibkr_client.py
- [X] T025 [P] [US4] Integration test for place_order, modify_order, and cancel_order tools in tests/integration/test_order_tools.py

**Checkpoint**: User Story 4 functional - Full trading lifecycle enabled.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Quality assurance, performance targets, and documentation

- [X] T030 [P] Implement "slow request" warning logic (> 2s) and append to tool outputs (SC-002) in src/mcp_server/utils.py or middleware
- [X] T031 Finalize README.md with comprehensive tool usage examples
- [X] T032 [P] Create performance verification script to validate SC-002 latency targets in scripts/perf-check.py
- [X] T033 [P] Final test run to verify 90% coverage requirement is met across all packages
- [X] T034 Verify and finalize docs/setup.md and quickstart.md consistency (FR-001)
- [X] T035 [P] Add uvx remote execution support and update documentation
