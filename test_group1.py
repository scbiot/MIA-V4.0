import logging
import sys
import os

# Ensure src is in path
sys.path.append(os.getcwd())

from src.scraper import Scraper

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def test_group1_search():
    logger.info("Initializing Scraper...")
    try:
        scraper = Scraper()
    except Exception as e:
        logger.error(f"Failed to initialize scraper: {e}")
        return

    logger.info("Starting Group 1 Search Test...")
    
    # Filter to only Group 1 portals for this test to avoid noise
    target_portals = ["Comprar (Nacional)", "Contratar (Obra Publica)", "Boletin Oficial"]
    
    results = []
    
    for portal_config in scraper.portals:
        if portal_config['name'] not in target_portals:
            continue
            
        if not portal_config.get('enabled', False):
            logger.info(f"Skipping {portal_config['name']} (Disabled)")
            continue

        logger.info(f"Testing {portal_config['name']}...")
        searcher = scraper._get_searcher(portal_config)
        
        if not searcher:
            logger.error(f"FAIL: No searcher found for {portal_config['name']}")
            continue
            
        try:
            # Search with a few known keywords to trigger a hit if possible
            # keywords are already loaded in scraper.all_keywords
            # We use a subset to test
            test_keywords = ["Licitación", "Pliego", "Agua"] 
            
            ops = searcher.search(test_keywords)
            logger.info(f"  Found {len(ops)} results.")
            
            if ops:
                for op in ops:
                    logger.info(f"    - Title: {op.get('title', 'No Title')}")
                    logger.info(f"    - URL: {op.get('url')}")
                    logger.info(f"    - Snippet: {op.get('content_snippet')[:100]}...")
            else:
                logger.warning(f"  No results found. (This might be valid if no keywords match)")
                
        except Exception as e:
            logger.error(f"FAIL: Error searching {portal_config['name']}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_group1_search()
