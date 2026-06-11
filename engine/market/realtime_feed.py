import aiohttp
import asyncio

class RealtimeMarketFeedEngine:
    async def _fetch_ticker(self, session: aiohttp.ClientSession, ticker: str) -> dict:
        url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d"
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            async with session.get(url, headers=headers, timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    meta = data.get('chart', {}).get('result', [{}])[0].get('meta', {})
                    price = meta.get('regularMarketPrice', 'N/A')
                    vol = meta.get('regularMarketVolume', 'N/A')
                    return {"ticker": ticker, "price": price, "volume": vol}
                return {"ticker": ticker, "price": "N/A", "volume": "N/A"}
        except Exception:
            return {"ticker": ticker, "price": "N/A", "volume": "N/A"}

    async def _fetch_all(self, tickers: list[str]) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch_ticker(session, t) for t in tickers]
            return await asyncio.gather(*tasks)

    def calculate(self, ticker_symbols: str) -> dict:
        """
        Pulls live market stock data (Current Price, Daily Volume) 
        for comma-separated ticker symbols (e.g., 'NEE, TSLA, ENPH, GE').
        """
        try:
            tickers = [t.strip().upper() for t in ticker_symbols.split(',')]
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(self._fetch_all(tickers))
            loop.close()

            results_text = "**[LIVE API] REAL-TIME ENERGY MARKET TELEMETRY:**\n\n"
            chart_data_series = []
            
            for res in results:
                ticker = res['ticker']
                price = res['price']
                vol = res['volume']
                
                if price != 'N/A':
                    chart_data_series.append({
                        "name": ticker,
                        "value": float(price)
                    })
                
                vol_formatted = f"{vol:,}" if isinstance(vol, int) else vol
                results_text += f"- **{ticker}**: Price: ${price} | Volume: {vol_formatted}\n"
                
            results_text += "\n> Data provided by direct market API. Prices reflect current conditions."
            
            chart_data = None
            if chart_data_series:
                chart_data = {
                    "type": "bar",
                    "data": {
                        "labels": [d["name"] for d in chart_data_series],
                        "datasets": [{
                            "label": "Live Stock Price (USD)",
                            "data": [d["value"] for d in chart_data_series]
                        }]
                    }
                }
                
            return {
                "status": "success",
                "result": results_text,
                "chart_data": chart_data
            }
            
        except Exception as e:
            return {"status": "error", "result": f"Real-Time API fetch failed: {str(e)}"}
