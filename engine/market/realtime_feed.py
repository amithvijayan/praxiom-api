import requests

class RealtimeMarketFeedEngine:
    def _fetch_ticker(self, ticker: str) -> dict:
        url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d"
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                meta = data.get('chart', {}).get('result', [{}])[0].get('meta', {})
                price = meta.get('regularMarketPrice', 'N/A')
                vol = meta.get('regularMarketVolume', 'N/A')
                return {"ticker": ticker, "price": price, "volume": vol}
            return {"ticker": ticker, "price": "N/A", "volume": "N/A"}
        except Exception:
            return {"ticker": ticker, "price": "N/A", "volume": "N/A"}

    def calculate(self, ticker_symbols: str) -> dict:
        """
        Pulls live market stock data (Current Price, Daily Volume) 
        for comma-separated ticker symbols (e.g., 'NEE, TSLA, ENPH, GE').
        """
        try:
            tickers = [t.strip().upper() for t in ticker_symbols.split(',')]
            
            # Fetch sequentially using lightweight synchronous requests
            # This completely avoids asyncio event loop conflicts in FastAPI's ThreadPool
            results = [self._fetch_ticker(t) for t in tickers]

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

