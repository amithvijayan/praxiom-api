import yfinance as yf

class RealtimeMarketFeedEngine:
    def calculate(self, ticker_symbols: str) -> dict:
        """
        Pulls live market stock data (Current Price, Market Cap, Daily Volume) 
        for comma-separated ticker symbols (e.g., 'NEE, TSLA, ENPH, GE').
        """
        try:
            tickers = [t.strip() for t in ticker_symbols.split(',')]
            results_text = "**[LIVE API] REAL-TIME ENERGY MARKET TELEMETRY:**\n\n"
            
            chart_data_series = []
            
            for ticker in tickers:
                stock = yf.Ticker(ticker)
                info = stock.info
                
                # Note: yfinance .info can sometimes be slow or miss data. We use fallback values.
                current_price = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
                market_cap = info.get('marketCap', 0)
                volume = info.get('volume', 0)
                
                if current_price != 'N/A':
                    chart_data_series.append({
                        "name": ticker,
                        "value": float(current_price)
                    })
                
                mc_formatted = f"${market_cap / 1e9:.2f}B" if market_cap else "N/A"
                
                results_text += f"- **{ticker.upper()}**: Price: ${current_price} | Market Cap: {mc_formatted} | Volume: {volume:,}\n"
                
            results_text += "\n> Data provided by yfinance. Prices reflect current market conditions."
            
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
