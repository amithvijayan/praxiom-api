import asyncio
from engine.market.realtime_feed import RealtimeMarketFeedEngine

async def test():
    engine = RealtimeMarketFeedEngine()
    print("Testing via to_thread...")
    res = await asyncio.to_thread(engine.calculate, "TSLA, NEE, ENPH")
    print(res)

if __name__ == "__main__":
    asyncio.run(test())
