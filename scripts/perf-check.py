import asyncio
import sys
import time
from pathlib import Path
from unittest.mock import AsyncMock, patch

# Add src to sys.path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from ibkr.models import Position
from mcp_server.tools import get_positions


async def check_latency_warning():
    print("Testing latency warning (SC-002)...")

    # Mock a slow client response (2.5 seconds)
    mock_positions = [Position(conid=12345, symbol="AAPL", size=100)]

    with patch("mcp_server.tools.get_client") as mock_get_client:
        mock_client = AsyncMock()

        async def slow_get_positions(_account_id):
            await asyncio.sleep(2.1)  # Threshold is 2.0s
            return mock_positions

        mock_client.get_positions.side_effect = slow_get_positions
        mock_get_client.return_value = mock_client
        
        print("Calling get_positions (expecting > 2s delay)...")
        start = time.perf_counter()
        result = await get_positions("U12345")
        duration = time.perf_counter() - start
        
        print(f"Call took {duration:.2f}s")
        print(f"Result preview: {result[:100]}...")
        
        if "WARNING: Request took" in result:
            print("✅ SUCCESS: Latency warning appended correctly.")
        else:
            print("❌ FAILURE: Latency warning missing from output.")
            exit(1)

if __name__ == "__main__":
    asyncio.run(check_latency_warning())
