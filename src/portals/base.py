import logging
import requests
from abc import ABC, abstractmethod

class PortalSearcher(ABC):
    """
    Abstract base class for all portal searchers.
    """
    def __init__(self, portal_config):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.name = portal_config.get("name")
        self.base_url = portal_config.get("url")
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })

    @abstractmethod
    def search(self, keywords):
        """
        Search the portal for opportunities matching the keywords.
        
        Args:
            keywords (list): List of keyword strings to search for.
            
        Returns:
            list: A list of result dictionaries. Each dictionary should have at least:
                  - 'portal': str
                  - 'title': str (optional but good)
                  - 'url': str
                  - 'content_snippet': str
                  - 'full_text': str
        """
        pass

    def fetch_page(self, url):
        """Helper to fetch a page with error handling."""
        try:
            resp = self.session.get(url, timeout=20)
            resp.raise_for_status()
            return resp
        except Exception as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None
