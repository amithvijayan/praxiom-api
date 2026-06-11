import asyncio
from engine.market.realtime_feed import RealtimeMarketFeedEngine

async def test():
    engine = RealtimeMarketFeedEngine()
    print("Testing engine.calculate...")
    res = engine.calculate("TSLA, NEE, ENPH")
    print(res)

if __name__ == "__main__":
    asyncio.run(test())
