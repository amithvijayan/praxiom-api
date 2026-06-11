import asyncio
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import logging
from engine.memory.vector_memory import VectorMemoryVault

logger = logging.getLogger(__name__)

class DeepResearchEngine:
    def __init__(self):
        self.memory = VectorMemoryVault.get_instance()

    def fetch_url_text(self, url: str) -> str:
        """Fetches and extracts text from a URL using BeautifulSoup."""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Remove scripts and styles
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
                
            text = soup.get_text(separator="\n")
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = "\n".join(chunk for chunk in chunks if chunk)
            return text
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {str(e)}")
            return ""

    def calculate(self, query: str, max_results: int = 3) -> str:
        """
        Omniscient Web Crawler: Searches DuckDuckGo, scrapes the URLs, 
        and permanently memorizes the content in Pinecone.
        """
        logger.info(f"[DEEP RESEARCH] Searching web for: {query}")
        
        try:
            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=max_results):
                    results.append(r)
            
            if not results:
                return f"No web search results found for: {query}"
                
            total_memorized = 0
            sources = []
            
            for res in results:
                title = res.get('title', 'Unknown Title')
                url = res.get('href', '')
                snippet = res.get('body', '')
                
                if not url:
                    continue
                    
                sources.append(url)
                logger.info(f"[DEEP RESEARCH] Scraping: {url}")
                
                content = self.fetch_url_text(url)
                
                # Fallback to snippet if scraping fails or is blocked
                if len(content) < 100:
                    content = snippet
                    
                # Add context string
                knowledge = f"SOURCE: {url}\nTITLE: {title}\nCONTENT:\n{content}"
                
                # Ingest into Pinecone (limited to 5 chunks per URL to prevent OOM/timeouts)
                chunks = self.memory.ingest_text(knowledge, url_source=url, max_chunks=5)
                total_memorized += len(chunks)
                
            return (
                f"> **[PASS] OMNISCIENT ASSIMILATION COMPLETE**\n"
                f"Successfully crawled {len(sources)} sources from the web.\n"
                f"- **Query**: {query}\n"
                f"- **Sources**: {', '.join(sources)}\n"
                f"- **Data Burned to Pinecone**: {total_memorized} discrete mathematical/semantic chunks permanently memorized."
            )
            
        except Exception as e:
            logger.error(f"[DEEP RESEARCH] Error: {str(e)}")
            return f"> **[WARNING] DEEP RESEARCH FAILED**\nError during web assimilation: {str(e)}"
