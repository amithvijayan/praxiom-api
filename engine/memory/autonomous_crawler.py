import urllib.request
from bs4 import BeautifulSoup
from engine.registry import EngineRegistry
from engine.memory.vector_memory import VectorMemoryVault

@EngineRegistry.register("web_crawler")
class AutonomousCrawler:
    """
    Crawls web URLs, extracts the pure text, and securely injects it 
    into Praxiom's Pinecone Vector Memory. Use this tool if the user asks you 
    to read, ingest, or learn from a specific URL.
    """
    
    def calculate(self, url: str, title: str = "Ingested Document"):
        print(f"Autonomous Crawler initializing on: {url}")
        try:
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) PraxiomCrawler/1.0'}
            )
            with urllib.request.urlopen(req) as response:
                html = response.read().decode('utf-8', errors='ignore')
                
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove scripts and styles
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
                
            text = soup.get_text(separator=' ', strip=True)
            
            # Basic validation
            if len(text) < 100:
                return {"status": "error", "message": "Not enough text extracted from URL."}
                
            # Initialize Vault and Memorize
            vault = VectorMemoryVault.get_instance()
            chunks_saved = vault.memorize_document(text=text, source_url=url, title=title)
            
            return {
                "result_text": f"Successfully ingested {title} from {url}. Memorized {chunks_saved} discrete mathematical chunks into Pinecone Permanent Memory.",
                "chart_data": None
            }
            
        except Exception as e:
            return {
                "result_text": f"Crawler Error: {str(e)}",
                "chart_data": None
            }
