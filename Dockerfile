# syntax=docker/dockerfile:1.7
# ──────────────────────────────────────────────────────────────────────────────
# Stage 1 – builder
#   Installs runtime dependencies into an isolated venv using uv so nothing
#   spills into the final image.
# ──────────────────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install uv – the project's canonical package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /build

# Copy only the dependency manifests first for optimal layer caching.
COPY pyproject.toml uv.lock ./

# Sync runtime deps only into /build/.venv (no dev extras, frozen lockfile).
RUN uv sync --frozen --no-dev --no-editable

# Now copy application source.
COPY src/ ./src/

# ──────────────────────────────────────────────────────────────────────────────
# Stage 2 – runtime
#   Minimal image: no build tools, uv binary, or source files beyond src/.
# ──────────────────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

# --------------------------------------------------------------------------- #
# Security hardening                                                           #
# --------------------------------------------------------------------------- #

# 1. Non-root user
RUN groupadd --system --gid 1001 appgroup && \
    useradd  --system --uid 1001 --gid 1001 --no-create-home appuser

# 2. Strip SUID/SGID bits inherited from the base image
RUN find / -xdev \( -perm -4000 -o -perm -2000 \) -exec chmod ug-s {} \; 2>/dev/null || true

# 3. Runtime environment – no bytecode, unbuffered I/O (critical for stdio MCP)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONIOENCODING=utf-8 \
    HISTFILE=/dev/null

WORKDIR /app

# Copy the pre-built venv and application source from the builder.
COPY --from=builder --chown=appuser:appgroup /build/.venv  /app/.venv
COPY --from=builder --chown=appuser:appgroup /build/src    /app/src

# Activate the venv by prepending its bin/ to PATH.
ENV VIRTUAL_ENV=/app/.venv \
    PATH=/app/.venv/bin:$PATH \
    PYTHONPATH=/app/src

USER appuser

# --------------------------------------------------------------------------- #
# Image metadata (OCI annotations)                                             #
# --------------------------------------------------------------------------- #
LABEL org.opencontainers.image.title="ibkr-mcp" \
      org.opencontainers.image.description="MCP server for Interactive Brokers Client Portal API" \
      org.opencontainers.image.source="https://github.com/rhollosy/ibkr-mcp" \
      org.opencontainers.image.licenses="MIT"

# --------------------------------------------------------------------------- #
# Health check – verifies the Python entry-point is importable                #
# --------------------------------------------------------------------------- #
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import mcp_server.server" || exit 1

# MCP servers communicate over stdio; no network port is needed for that.
# Uncomment if you switch to HTTP/SSE transport:
# EXPOSE 8000

ENTRYPOINT ["python", "/app/src/main.py"]
