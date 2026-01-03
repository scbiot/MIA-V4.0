"""
================================================================================
MIA V4.0 - SCRAPERS DE FASE 2A: PORTALES CRÍTICOS
================================================================================

OBJETIVO:
    Implementar scrapers específicos para los 4 portales críticos de Fase 2A:
    1. aysa.com.ar - Empresa de agua (100% relevante)
    2. opc.gba.gob.ar - Provincia de Buenos Aires
    3. buenosairescompras.gob.ar - Ciudad de Buenos Aires
    4. proveedores.ypf.com - YPF (análisis de viabilidad)

FASE: 2A - Portales Críticos
AUTOR: Water Tech S.A.
VERSIÓN: 4.0 - Fase 2A
FECHA: 2026-01-02
================================================================================
"""

import logging
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from .base import PortalSearcher

# ============================================================================
# CONFIGURACIÓN DE SELENIUM
# ============================================================================

def get_selenium_driver(headless=True):
    """
    Crea y configura un driver de Selenium para Chrome.
    
    PARÁMETROS:
        headless (bool): Si True, ejecuta Chrome sin interfaz gráfica
    
    RETORNO:
        webdriver.Chrome: Driver configurado
    """
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument('--headless')
    
    # Opciones para mejorar rendimiento y evitar detección
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    # Instalar y configurar driver automáticamente
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver


# ============================================================================
# PORTAL 1: AYSA.COM.AR - EMPRESA DE AGUA
# ============================================================================

class AysaScraper(PortalSearcher):
    """
    Scraper para aysa.com.ar - Agua y Saneamientos Argentinos
    
    PRIORIDAD: ⭐⭐⭐⭐⭐ CRÍTICA
    VALOR DE NEGOCIO: 🔴 MUY ALTO (100% alineado con el negocio)
    COMPLEJIDAD: 🟡 Media
    """
    
    def __init__(self, portal_config):
        super().__init__(portal_config)
        self.licitaciones_url = f"{self.base_url}/licitaciones"
        self.logger.info(f"Inicializado scraper para {self.name}")
    
    def search(self, keywords):
        """
        Busca licitaciones en AySA que coincidan con las keywords.
        
        ESTRATEGIA:
            1. Acceder a ambas secciones de licitaciones:
               - Obras de Infraestructura
               - Bienes, Servicios y Obras de Mejora
            2. Hacer click en botón "BUSCAR" para cargar resultados
            3. Filtrar por keywords si es necesario
            4. Extraer datos de la tabla de resultados
            5. Obtener detalles de cada licitación
        
        PARÁMETROS:
            keywords (list): Lista de palabras clave a buscar
        
        RETORNO:
            list: Lista de oportunidades encontradas
        """
        self.logger.info(f"Buscando en {self.name} con keywords: {keywords}")
        results = []
        
        # URLs de las dos secciones de licitaciones
        sections = [
            {
                "name": "Obras de Infraestructura",
                "url": "https://aysa.com.ar/proveedores/licitaciones/licitaciones_infraestructura/"
            },
            {
                "name": "Bienes, Servicios y Obras de Mejora",
                "url": "https://aysa.com.ar/proveedores/licitaciones/Licitaciones-Bienes-Servicios/"
            }
        ]
        
        # Usar Selenium para interactuar con el portal
        driver = None
        try:
            from src.portals.phase2a import get_selenium_driver
            driver = get_selenium_driver(headless=True)
            
            for section in sections:
                self.logger.info(f"Escaneando sección: {section['name']}")
                
                try:
                    # Navegar a la sección
                    driver.get(section['url'])
                    time.sleep(2)  # Esperar carga de página
                    
                    # Hacer click en botón BUSCAR para cargar resultados
                    search_button = driver.find_element(By.ID, "btnSearch")
                    search_button.click()
                    time.sleep(3)  # Esperar carga de resultados
                    
                    # Extraer resultados de la tabla
                    section_results = self._extract_tender_results(driver, keywords, section['name'])
                    results.extend(section_results)
                    
                    self.logger.info(f"Encontradas {len(section_results)} oportunidades en {section['name']}")
                    
                except Exception as e:
                    self.logger.error(f"Error en sección {section['name']}: {e}")
                    continue
            
        except Exception as e:
            self.logger.error(f"Error en scraper de {self.name}: {e}")
        finally:
            if driver:
                driver.quit()
        
        self.logger.info(f"Total encontradas: {len(results)} oportunidades en {self.name}")
        return results
    
    def _extract_tender_results(self, driver, keywords, section_name):
        """
        Extrae resultados de licitaciones de la tabla.
        
        PARÁMETROS:
            driver: WebDriver de Selenium
            keywords (list): Keywords para filtrar
            section_name (str): Nombre de la sección
        
        RETORNO:
            list: Lista de oportunidades extraídas
        """
        results = []
        
        try:
            # Buscar tabla de resultados
            # La tabla está dentro de un contenedor con clase específica
            table_rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
            
            for row in table_rows:
                try:
                    # Extraer datos de cada columna
                    cells = row.find_elements(By.TAG_NAME, "td")
                    
                    if len(cells) < 4:
                        continue
                    
                    # Estructura de la tabla:
                    # 0: Estado
                    # 1: N° Licitación
                    # 2: Objeto (descripción)
                    # 3: Fechas
                    # 4: Presupuesto
                    
                    estado = cells[0].text.strip()
                    numero = cells[1].text.strip()
                    objeto = cells[2].text.strip()
                    fechas = cells[3].text.strip() if len(cells) > 3 else ""
                    presupuesto = cells[4].text.strip() if len(cells) > 4 else "No aplica"
                    
                    # Filtrar por keywords si se especificaron
                    if keywords:
                        texto_completo = f"{objeto} {numero}".lower()
                        if not any(kw.lower() in texto_completo for kw in keywords):
                            continue
                    
                    # Intentar obtener URL de detalle (si la fila es clickeable)
                    detail_url = ""
                    try:
                        # Buscar enlace en la fila
                        link = row.find_element(By.TAG_NAME, "a")
                        detail_url = link.get_attribute("href")
                    except:
                        detail_url = f"https://aysa.com.ar/proveedores/licitaciones/"
                    
                    # Crear resultado
                    result = {
                        "portal": self.name,
                        "section": section_name,
                        "title": f"{numero} - {objeto}",
                        "numero_licitacion": numero,
                        "objeto": objeto,
                        "estado": estado,
                        "fechas": fechas,
                        "presupuesto": presupuesto,
                        "url": detail_url,
                        "content_snippet": objeto[:200],
                        "full_text": f"Licitación {numero}: {objeto}. Estado: {estado}. Fechas: {fechas}. Presupuesto: {presupuesto}",
                        "matched_keywords": [kw for kw in keywords if kw.lower() in objeto.lower()] if keywords else []
                    }
                    
                    results.append(result)
                    
                except Exception as e:
                    self.logger.debug(f"Error extrayendo fila: {e}")
                    continue
            
        except Exception as e:
            self.logger.error(f"Error extrayendo resultados de tabla: {e}")
        
        return results


# ============================================================================
# PORTAL 2: OPC.GBA.GOB.AR - PROVINCIA DE BUENOS AIRES
# ============================================================================

class OpcGbaScraper(PortalSearcher):
    """
    Scraper para opc.gba.gob.ar - Oficina Provincial de Contrataciones
    
    PRIORIDAD: ⭐⭐⭐⭐⭐ CRÍTICA
    VALOR DE NEGOCIO: 🔴 MUY ALTO (Provincia más grande de Argentina)
    COMPLEJIDAD: 🟡 Media
    """
    
    def __init__(self, portal_config):
        super().__init__(portal_config)
        self.logger.info(f"Inicializado scraper para {self.name}")
    
    def search(self, keywords):
        """
        Busca licitaciones en OPC GBA que coincidan con las keywords.
        
        ESTRATEGIA:
            1. Usar buscador del portal
            2. Aplicar filtros por keywords
            3. Extraer resultados paginados
            4. Obtener detalles de cada licitación
        
        PARÁMETROS:
            keywords (list): Lista de palabras clave a buscar
        
        RETORNO:
            list: Lista de oportunidades encontradas
        """
        self.logger.info(f"Buscando en {self.name} con keywords: {keywords}")
        results = []
        
        try:
            # TODO: Implementar lógica específica de OPC GBA
            self.logger.warning(f"Scraper de {self.name} aún no implementado completamente")
            
        except Exception as e:
            self.logger.error(f"Error en scraper de {self.name}: {e}")
        
        self.logger.info(f"Encontradas {len(results)} oportunidades en {self.name}")
        return results


# ============================================================================
# PORTAL 3: BUENOSAIRESCOMPRAS.GOB.AR - CIUDAD DE BUENOS AIRES
# ============================================================================

class BuenosAiresComprasScraper(PortalSearcher):
    """
    Scraper para buenosairescompras.gob.ar - Portal de Compras de CABA
    
    PRIORIDAD: ⭐⭐⭐⭐⭐ CRÍTICA
    VALOR DE NEGOCIO: 🔴 MUY ALTO (Ciudad de Buenos Aires)
    COMPLEJIDAD: 🟡 Media
    """
    
    def __init__(self, portal_config):
        super().__init__(portal_config)
        self.logger.info(f"Inicializado scraper para {self.name}")
    
    def search(self, keywords):
        """
        Busca licitaciones en Buenos Aires Compras que coincidan con las keywords.
        
        ESTRATEGIA:
            1. Navegar por categorías relevantes
            2. Buscar por keywords dentro de categorías
            3. Extraer listados de licitaciones
            4. Obtener detalles completos
        
        PARÁMETROS:
            keywords (list): Lista de palabras clave a buscar
        
        RETORNO:
            list: Lista de oportunidades encontradas
        """
        self.logger.info(f"Buscando en {self.name} con keywords: {keywords}")
        results = []
        
        try:
            # TODO: Implementar lógica específica de Buenos Aires Compras
            self.logger.warning(f"Scraper de {self.name} aún no implementado completamente")
            
        except Exception as e:
            self.logger.error(f"Error en scraper de {self.name}: {e}")
        
        self.logger.info(f"Encontradas {len(results)} oportunidades en {self.name}")
        return results


# ============================================================================
# PORTAL 4: PROVEEDORES.YPF.COM - YPF (ANÁLISIS DE VIABILIDAD)
# ============================================================================

class YpfScraper(PortalSearcher):
    """
    Scraper para proveedores.ypf.com - Portal de Proveedores de YPF
    
    PRIORIDAD: ⭐⭐⭐⭐⭐ CRÍTICA
    VALOR DE NEGOCIO: 🔴 MUY ALTO (Grandes proyectos)
    COMPLEJIDAD: 🔴 Alta (requiere autenticación)
    
    NOTA: Este scraper requiere análisis de viabilidad.
          Puede requerir credenciales de proveedor.
    """
    
    def __init__(self, portal_config):
        super().__init__(portal_config)
        self.requires_auth = True
        self.logger.info(f"Inicializado scraper para {self.name}")
        self.logger.warning(f"{self.name} puede requerir autenticación")
    
    def search(self, keywords):
        """
        Busca licitaciones en YPF que coincidan con las keywords.
        
        ESTRATEGIA:
            1. Verificar si existe sección pública
            2. Si requiere auth, documentar limitación
            3. Si hay sección pública, implementar scraping
        
        PARÁMETROS:
            keywords (list): Lista de palabras clave a buscar
        
        RETORNO:
            list: Lista de oportunidades encontradas (puede estar vacía)
        """
        self.logger.info(f"Buscando en {self.name} con keywords: {keywords}")
        results = []
        
        try:
            # TODO: Análisis de viabilidad
            # Verificar si requiere autenticación obligatoria
            self.logger.warning(f"Scraper de {self.name} requiere análisis de viabilidad")
            self.logger.info(f"Verificando si {self.name} tiene sección pública...")
            
        except Exception as e:
            self.logger.error(f"Error en scraper de {self.name}: {e}")
        
        self.logger.info(f"Encontradas {len(results)} oportunidades en {self.name}")
        return results


# ============================================================================
# FACTORY FUNCTION - CREAR SCRAPER SEGÚN PORTAL
# ============================================================================

def create_phase2a_scraper(portal_config):
    """
    Factory function para crear el scraper apropiado según el portal.
    
    PARÁMETROS:
        portal_config (dict): Configuración del portal
    
    RETORNO:
        PortalSearcher: Instancia del scraper apropiado
    """
    portal_name = portal_config.get('name', '').lower()
    
    scraper_map = {
        'aysa.com.ar': AysaScraper,
        'opc.gba.gob.ar': OpcGbaScraper,
        'buenosairescompras.gob.ar': BuenosAiresComprasScraper,
        'proveedores.ypf.com': YpfScraper
    }
    
    scraper_class = scraper_map.get(portal_name)
    
    if scraper_class:
        return scraper_class(portal_config)
    else:
        raise ValueError(f"No hay scraper implementado para: {portal_name}")


# ============================================================================
# UTILIDADES PARA SELENIUM
# ============================================================================

class SeleniumHelper:
    """
    Clase helper con utilidades comunes para Selenium.
    """
    
    @staticmethod
    def wait_for_element(driver, by, value, timeout=10):
        """
        Espera a que un elemento esté presente en la página.
        
        PARÁMETROS:
            driver: WebDriver de Selenium
            by: Tipo de selector (By.ID, By.CLASS_NAME, etc.)
            value: Valor del selector
            timeout: Tiempo máximo de espera en segundos
        
        RETORNO:
            WebElement o None si no se encuentra
        """
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception as e:
            logging.error(f"Elemento no encontrado: {value} - {e}")
            return None
    
    @staticmethod
    def safe_click(driver, element):
        """
        Click seguro en un elemento con manejo de errores.
        """
        try:
            element.click()
            return True
        except Exception as e:
            logging.error(f"Error al hacer click: {e}")
            return False
    
    @staticmethod
    def extract_text_safe(element):
        """
        Extrae texto de un elemento de forma segura.
        """
        try:
            return element.text.strip()
        except:
            return ""


# ============================================================================
# NOTAS DE IMPLEMENTACIÓN
# ============================================================================
"""
PRÓXIMOS PASOS:

1. INVESTIGACIÓN DE PORTALES:
   - Visitar cada portal manualmente
   - Identificar estructura HTML
   - Localizar sección de licitaciones
   - Analizar formularios de búsqueda

2. IMPLEMENTACIÓN POR PORTAL:
   - Comenzar con aysa.com.ar (más relevante)
   - Continuar con opc.gba.gob.ar
   - Luego buenosairescompras.gob.ar
   - Finalmente analizar viabilidad de YPF

3. TESTING:
   - Test unitario por cada scraper
   - Test de integración
   - Validación de datos extraídos

4. OPTIMIZACIÓN:
   - Agregar caché de páginas
   - Implementar rate limiting específico
   - Mejorar manejo de errores
"""
