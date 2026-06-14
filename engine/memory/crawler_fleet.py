import asyncio
import aiohttp
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from engine.memory.vector_memory import VectorMemoryVault
import logging

logger = logging.getLogger(__name__)

class AsyncCrawlerFleetEngine:
    def __init__(self):
        self.memory = VectorMemoryVault.get_instance()
        
    async def _fetch_url(self, session: aiohttp.ClientSession, url: str) -> str:
        """Asynchronously fetches text from a single URL."""
        try:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")
                    text = ' '.join(soup.stripped_strings)
                    return text[:5000] # Cap at 5000 chars per page
                return ""
        except Exception as e:
            logger.warning(f"Crawler failed on {url}: {str(e)}")
            return ""

    async def _crawl_swarm(self, urls: list[str]) -> list[str]:
        """Deploys a swarm of async crawlers."""
        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch_url(session, url) for url in urls]
            return await asyncio.gather(*tasks)

    def calculate(self, search_query: str, num_results: int = 10) -> dict:
        """
        Deploys an asynchronous swarm of web crawlers to scrape the top N search results 
        simultaneously and bulk-upsert the extracted knowledge into Pinecone Vector Memory.
        """
        try:
            logger.info(f"Deploying crawler fleet for query: '{search_query}' (N={num_results})")
            
            # 1. Search DuckDuckGo
            ddgs = DDGS()
            results = list(ddgs.text(search_query, max_results=num_results))
            
            if not results:
                return {"status": "error", "result": "Search yielded no results."}
                
            urls = [r["href"] for r in results]
            
            # 2. Deploy Async Swarm
            # Run the async loop inside the synchronous calculate method
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            scraped_texts = loop.run_until_complete(self._crawl_swarm(urls))
            loop.close()
            
            # 3. Filter empty results
            valid_texts = [t for t in scraped_texts if len(t) > 100]
            
            # 4. Bulk Upsert into Memory
            total_vectors = 0
            for i, text in enumerate(valid_texts):
                chunks_stored = self.memory.memorize_document(
                    text=text,
                    source_url=urls[i],
                    title=f"Swarm Intel: {search_query}"
                )
                total_vectors += chunks_stored
                
            result_text = (
                f"> **[SWARM ACTIVE] MASSIVE WEB CRAWLER FLEET**\n"
                f"- **Target Query**: '{search_query}'\n"
                f"- **Agents Deployed**: {len(urls)} concurrent crawlers\n"
                f"- **Successful Extractions**: {len(valid_texts)}\n"
                f"- **Knowledge Vectors Stored**: {total_vectors} chunks pushed to Pinecone\n\n"
                f"Praxiom has achieved enhanced understanding of this domain."
            )
            
            chart_data = {
                "type": "bar",
                "data": {
                    "labels": ["Agents Deployed", "Successful Extractions", "Vectors Stored"],
                    "datasets": [{
                        "label": "Crawler Swarm Telemetry",
                        "data": [len(urls), len(valid_texts), total_vectors]
                    }]
                }
            }
            
            return {
                "status": "success",
                "result": result_text,
                "chart_data": chart_data
            }
            
        except Exception as e:
            return {"status": "error", "result": f"Crawler Swarm failed: {str(e)}"}
