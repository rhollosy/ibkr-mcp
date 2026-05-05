<!--
Sync Impact Report:
- Version change: [CONSTITUTION_VERSION] → 1.0.0
- List of modified principles:
    - [PRINCIPLE_1_NAME] → I. Library-First Integration
    - [PRINCIPLE_2_NAME] → II. Test-Driven Quality (>= 90% Coverage)
    - [PRINCIPLE_3_NAME] → III. FastMCP Architecture
    - [PRINCIPLE_4_NAME] → IV. Secure Authentication Delegation
    - [PRINCIPLE_5_NAME] → V. Modern Python Tooling (uv) (Added)
- Added sections: Technical Constraints, Development Workflow
- Removed sections: None
- Templates requiring updates:
    - ✅ .specify/templates/plan-template.md
    - ✅ .specify/templates/spec-template.md
    - ✅ .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->

# ibkr-mcp Constitution

## Core Principles

### I. Library-First Integration
Business logic and IBKR API interaction MUST be decoupled from MCP tool definitions. Libraries must be self-contained, independently testable, and well-documented. This ensures that the core trading logic can be reused outside of the MCP context if necessary.

### II. Test-Driven Quality (>= 90% Coverage)
TDD is non-negotiable. Tests must be written and verified to fail before any implementation code is added. Every feature must reach at least 90% test coverage before it is considered complete. Red-Green-Refactor cycles are strictly enforced.

### III. FastMCP Architecture
Use the FastMCP framework for building the server. Leverage decorators and high-level abstractions to expose tools and resources. Keep the MCP server layer thin, delegating all complex logic to the underlying library modules.

### IV. Secure Authentication Delegation
The server delegates all authentication and 2FA concerns to the official IBKR Client Portal API Gateway. The MCP server MUST NOT attempt to automate credential entry or bypass 2FA. It should provide tools to check status and guide the user to the gateway's native authentication UI.

### V. Modern Python Tooling (uv)
Use `uv` as the primary package and environment manager. This ensures deterministic, high-performance builds and standardized developer environments across the project. All dependency management and environment creation MUST use `uv` commands.

## Technical Constraints

The project is built using Python 3.11+, FastMCP, and `httpx` for asynchronous communication. It requires the IBKR Client Portal API Gateway to be running locally on a predefined port. All external API calls MUST be asynchronous.

## Development Workflow

The development follows a strict sequential order: Specification -> Planning -> Task Generation -> Implementation. Each user story must be implemented as an independent, testable increment. All PRs must include a coverage report verifying the 90% threshold.

## Governance

This constitution supersedes all other project practices. Amendments require a documented rationale, a version increment (Semantic Versioning), and a migration plan if existing principles are modified. Compliance is verified during code reviews and automated CI gates.

**Version**: 1.0.0 | **Ratified**: 2026-04-30 | **Last Amended**: 2026-04-30
