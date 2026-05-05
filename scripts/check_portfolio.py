
import asyncio
import os
import sys
from pathlib import Path

# Add src to sys.path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from ibkr.client import IBKRClient

async def main():
    base_url = os.getenv("IBKR_GATEWAY_URL", "https://localhost:5001/v1/api")
    client = IBKRClient(base_url=base_url)
    
    try:
        # Check auth
        auth = await client.get_auth_status()
        if not auth.get("authenticated"):
            print("Not authenticated. Please log in to IBKR Gateway.")
            return

        # Get accounts
        accounts = await client.get_accounts()
        if not accounts:
            print("No accounts found.")
            return

        for acc in accounts:
            acc_id = acc["accountId"]
            print(f"\nAccount: {acc_id}")
            positions = await client.get_positions(acc_id)
            if not positions:
                print("  No positions.")
                continue
            
            for p in positions:
                symbol = p.get("contractDesc") or p.get("symbol") or "Unknown"
                pos = p.get("position", 0)
                mkt_price = p.get("mktPrice", 0)
                mkt_val = p.get("mktValue", 0)
                print(f"  - {symbol}: {pos} @ {mkt_price} (Value: {mkt_val})")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
