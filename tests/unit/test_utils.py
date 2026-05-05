import asyncio

import pytest

from mcp_server.utils import warn_if_slow


@pytest.mark.asyncio
async def test_warn_if_slow_no_warning():
    @warn_if_slow(threshold=0.5)
    async def fast_func():
        return "result"
    
    res = await fast_func()
    assert res == "result"

@pytest.mark.asyncio
async def test_warn_if_slow_with_warning():
    @warn_if_slow(threshold=0.1)
    async def slow_func():
        await asyncio.sleep(0.2)
        return "result"
    
    res = await slow_func()
    assert "result" in res
    assert "WARNING: Request took" in res

@pytest.mark.asyncio
async def test_warn_if_slow_non_string():
    @warn_if_slow(threshold=0.1)
    async def slow_non_string():
        await asyncio.sleep(0.2)
        return {"data": 123}
    
    res = await slow_non_string()
    assert res == {"data": 123}
