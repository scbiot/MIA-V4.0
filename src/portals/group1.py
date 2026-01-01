from .base import PortalSearcher
from bs4 import BeautifulSoup
import time

class ComprarSearcher(PortalSearcher):
    """
    Searcher for comprar.gob.ar
    Strategy: Since deep search often requires complex form state, we will:
    1. Scan the main page for recent/featured processes.
    2. Attempt to construct a direct search URL if a pattern is found (TBD).
    For Stage 1, we will visit the main public access points.
    """
    def search(self, keywords):
        results = []
        # Main public page often lists recent tenders or has a "Processos de Compra" link
        # The URL for public search is usually: https://comprar.gob.ar/PLIEGO/BusquedaPliego.aspx or similar
        # For now, we scan the home page and potentially a known listing page if accessible.
        
        target_urls = [
            self.base_url,
            f"{self.base_url}/PLIEGO/BusquedaPliego.aspx" # Common pattern
        ]
        
        for url in target_urls:
            resp = self.fetch_page(url)
            if not resp:
                continue
                
            soup = BeautifulSoup(resp.text, 'html.parser')
            text_content = soup.get_text().lower()
            
            # Very basic check: do any keywords appear in the valid text?
            # Ideally we would loop through rows of a table.
            
            hit = False
            matched_kw = []
            for kw in keywords:
                if kw.lower() in text_content:
                    hit = True
                    matched_kw.append(kw)
            
            if hit:
                # We found keywords on the page. 
                # Since we are not strictly parsing individual rows yet (requires detailed HTML analysis),
                # we return the page itself as a "Lead" to be analyzed by the LLM.
                results.append({
                    "portal": self.name,
                    "url": url,
                    "title": f"Matches for {', '.join(matched_kw)}",
                    "content_snippet": soup.get_text()[:3000].strip(),
                    "full_text": soup.get_text()
                })
        
        return results

class ContratarSearcher(PortalSearcher):
    """
    Searcher for contratar.gob.ar
    Similar stack to Comprar.
    """
    def search(self, keywords):
        results = []
        resp = self.fetch_page(self.base_url)
        if not resp:
            return results
            
        soup = BeautifulSoup(resp.text, 'html.parser')
        text_content = soup.get_text().lower()
        
        matched_kw = [kw for kw in keywords if kw.lower() in text_content]
        
        if matched_kw:
             results.append({
                "portal": self.name,
                "url": self.base_url,
                "title": f"Home Page Match: {', '.join(matched_kw)}",
                "content_snippet": soup.get_text()[:3000].strip(),
                "full_text": soup.get_text()
            })
        return results

class BoletinSearcher(PortalSearcher):
    """
    Searcher for boletinoficial.gob.ar
    Has a specific section for announcements.
    """
    def search(self, keywords):
        results = []
        # The 'Sección' lists usually have URLs like:
        # https://www.boletinoficial.gob.ar/seccion/tercera (Contrataciones)
        
        section_url = f"{self.base_url}/seccion/tercera"
        
        resp = self.fetch_page(section_url)
        if not resp:
            # Fallback to home if section fails
            resp = self.fetch_page(self.base_url)
            if not resp: return results

        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # In the Boletin, we might want to look at specific headers or links.
        # For now, we stick to the text-scan strategy for consistency with Stage 1 requirements.
        
        text_content = soup.get_text().lower()
        matched_kw = [kw for kw in keywords if kw.lower() in text_content]
        
        if matched_kw:
             results.append({
                "portal": self.name,
                "url": section_url if section_url else self.base_url,
                "title": f"Boletin Matches: {', '.join(matched_kw)}",
                "content_snippet": soup.get_text()[:3000].strip(),
                "full_text": soup.get_text()
            })
            
        return results
