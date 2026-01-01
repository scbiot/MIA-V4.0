"""
================================================================================
MIA V4.0 - MÓDULO DE SCRAPING (scraper.py)
================================================================================

OBJETIVO GENERAL:
    Realizar búsquedas automatizadas en portales de compras públicas para
    detectar oportunidades comerciales basándose en palabras clave específicas
    (TRIGGERS) definidas en la configuración.

ETAPA: 1 - SCRAPING

FUNCIONAMIENTO:
    1. Carga la lista de portales activos desde config.py (PORTALS)
    2. Carga las palabras clave de búsqueda desde config.py (TRIGGERS)
    3. Conecta a cada portal mediante HTTP GET
    4. Extrae el contenido de texto de la página
    5. Busca coincidencias con las palabras clave (triggers)
    6. Retorna lista de oportunidades detectadas con metadata

CONFIGURACIÓN REQUERIDA (config.py):
    - PORTALS: Lista de portales con URLs y configuración
    - TRIGGERS: Palabras clave que activan la detección de oportunidades

SALIDA:
    Lista de diccionarios con:
    - portal: Nombre del portal
    - url: URL de la oportunidad
    - matched_keywords: Lista de triggers encontrados
    - content_snippet: Primeros 5000 caracteres del contenido
    - full_text: Texto completo de la página

LIMITACIONES ACTUALES (Stage 1):
    - Conexión simple HTTP GET (sin autenticación)
    - No maneja JavaScript dinámico
    - No sigue enlaces internos
    - Búsqueda básica de texto (case-insensitive)

AUTOR: Water Tech S.A.
VERSIÓN: 4.0 - Stage 1
================================================================================
"""

import requests
from bs4 import BeautifulSoup
import json
import logging
import os
import time
import random
from functools import wraps
from typing import Optional, Dict, Any

# ============================================================================
# DECORADOR DE RETRY CON BACKOFF EXPONENCIAL
# ============================================================================
def retry_with_backoff(max_retries=3, base_delay=1, max_delay=16):
    """
    Decorador que implementa retry logic con backoff exponencial.
    
    PARÁMETROS:
        max_retries (int): Número máximo de reintentos
        base_delay (float): Delay base en segundos
        max_delay (float): Delay máximo en segundos
    
    FUNCIONAMIENTO:
        - Intento 1: delay = base_delay (1s)
        - Intento 2: delay = base_delay * 2 (2s)
        - Intento 3: delay = base_delay * 4 (4s)
        - Agrega jitter aleatorio para evitar thundering herd
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (requests.exceptions.ConnectionError, 
                        requests.exceptions.Timeout,
                        requests.exceptions.HTTPError) as e:
                    retries += 1
                    if retries >= max_retries:
                        raise
                    
                    # Calcular delay con backoff exponencial
                    delay = min(base_delay * (2 ** (retries - 1)), max_delay)
                    # Agregar jitter aleatorio (±25%)
                    jitter = delay * 0.25 * (random.random() * 2 - 1)
                    actual_delay = delay + jitter
                    
                    logger = logging.getLogger(__name__)
                    logger.warning(
                        f"Reintento {retries}/{max_retries} después de {actual_delay:.2f}s. "
                        f"Error: {type(e).__name__}: {str(e)}"
                    )
                    time.sleep(actual_delay)
            return None
        return wrapper
    return decorator

# ============================================================================
# CLASE SCRAPER - MOTOR DE BÚSQUEDA WEB
# ============================================================================
class Scraper:
    """
    Clase responsable de escanear portales web en busca de oportunidades.
    
    RESPONSABILIDADES:
        - Conectar a portales de compras públicas
        - Extraer contenido de texto de las páginas
        - Detectar palabras clave (triggers)
        - Retornar oportunidades encontradas
    """
    
    def __init__(self):
        """
        CONSTRUCTOR - Inicialización del Scraper
        
        ACCIONES:
            1. Configura el logger para registro de operaciones
            2. Carga PORTALS desde config.py (lista de sitios a escanear)
            3. Carga TRIGGERS desde config.py (palabras clave de búsqueda)
            4. Convierte triggers a minúsculas para búsqueda case-insensitive
        """
        self.logger = logging.getLogger(__name__)
        from src.config import PORTALS, TRIGGERS
        
        self.portals = PORTALS      # Lista de portales a escanear
        self.triggers = [t.lower() for t in TRIGGERS]  # Keywords en minúsculas
        
        # Configuración de scraping desde variables de entorno
        self.timeout = int(os.getenv('SCRAPER_TIMEOUT', '15'))
        self.max_retries = int(os.getenv('SCRAPER_MAX_RETRIES', '3'))
        self.delay_seconds = float(os.getenv('SCRAPER_DELAY_SECONDS', '2'))
        
        # User-Agent realista
        self.user_agent = os.getenv(
            'SCRAPER_USER_AGENT',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        # Headers HTTP realistas
        self.headers = {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'es-AR,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        self.logger.info(f"Scraper configurado: timeout={self.timeout}s, retries={self.max_retries}, delay={self.delay_seconds}s")
        
    # ========================================================================
    # MÉTODO PRINCIPAL: ESCANEAR TODOS LOS PORTALES
    # ========================================================================
    def search_all(self):
        """
        Itera sobre todos los portales activos y busca oportunidades.
        
        PROCESO:
            1. Filtra solo portales con enabled=True
            2. Escanea cada portal individualmente
            3. Acumula todas las oportunidades encontradas
            4. Maneja errores por portal (un error no detiene el proceso)
        
        RETORNO:
            Lista de oportunidades (diccionarios) encontradas en todos los portales
        """
        results = []
        for portal in self.portals:
            # Verificar si el portal está habilitado en la configuración
            if not portal.get("enabled", True):
                continue
            
            self.logger.info(f"Scanning {portal['name']}...")
            try:
                opportunities = self.scan_portal(portal)
                results.extend(opportunities)  # Agregar oportunidades encontradas
                
                # Rate limiting: delay entre portales
                if self.delay_seconds > 0:
                    time.sleep(self.delay_seconds)
                    
            except Exception as e:
                # Error en un portal no detiene el escaneo de otros
                self.logger.error(f"Error crítico scanning {portal['name']}: {type(e).__name__}: {str(e)}")
                self.logger.debug(f"Stack trace:", exc_info=True)
        return results

    # ========================================================================
    # MÉTODO: ESCANEAR UN PORTAL INDIVIDUAL
    # ========================================================================
    def scan_portal(self, portal):
        """
        Escanea un portal específico en busca de triggers.
        
        PARÁMETROS:
            portal (dict): Diccionario con configuración del portal
                          Debe contener: 'name', 'url', 'enabled'
        
        PROCESO:
            1. Realiza HTTP GET a la URL del portal
            2. Parsea HTML con BeautifulSoup
            3. Extrae texto completo de la página
            4. Busca coincidencias con triggers
            5. Si encuentra triggers, crea registro de oportunidad
        
        RETORNO:
            Lista de oportunidades encontradas en este portal
        """
        url = portal['url']
        found_ops = []  # Lista de oportunidades detectadas
        
        try:
            # ----------------------------------------------------------------
            # CONEXIÓN HTTP AL PORTAL CON RETRY LOGIC
            # ----------------------------------------------------------------
            self.logger.info(f"   Conectando a {url}...")
            resp = self._make_request(url)
            if resp and resp.status_code == 200:
                # ------------------------------------------------------------
                # EXTRACCIÓN Y ANÁLISIS DE CONTENIDO
                # ------------------------------------------------------------
                soup = BeautifulSoup(resp.text, 'html.parser')
                text_content = soup.get_text().lower()  # Texto en minúsculas
                
                # ------------------------------------------------------------
                # DETECCIÓN DE PALABRAS CLAVE (TRIGGERS)
                # ------------------------------------------------------------
                # Busca TODAS las keywords que aparecen en el contenido
                # Registra cada una para el análisis posterior con IA
                # ------------------------------------------------------------
                matched_keywords = []
                for trigger in self.triggers:
                    if trigger in text_content:
                        matched_keywords.append(trigger)
                
                if matched_keywords:
                   # ---------------------------------------------------------
                   # OPORTUNIDAD DETECTADA
                   # ---------------------------------------------------------
                   # Crea registro con toda la información relevante
                   # ---------------------------------------------------------
                   self.logger.info(f"   [!] Oportunidad detectada (Keywords: {', '.join(matched_keywords)})")
                   found_ops.append({
                       "portal": portal['name'],                    # Nombre del portal
                       "url": url,                                  # URL de la oportunidad
                       "matched_keywords": matched_keywords,        # Triggers encontrados
                       "content_snippet": soup.get_text()[:5000],  # Primeros 5000 chars
                       "full_text": soup.get_text()                # Texto completo para IA
                   })
                else:
                    self.logger.info("   [-] No se encontraron palabras clave.")
            elif resp:
                # Manejo específico de códigos HTTP
                self._handle_http_error(resp.status_code, url)
            else:
                self.logger.error(f"   [ERROR] No se pudo obtener respuesta de {url}")
                
        # ====================================================================
        # MANEJO DE ERRORES DE CONEXIÓN
        # ====================================================================
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            # Errores comunes: DNS no resuelve, timeout, sitio caído
            self.logger.warning(
                f"   [ALERTA] No se pudo conectar a {url} después de {self.max_retries} intentos. "
                f"Error: {type(e).__name__}: {str(e)}"
            )
        except requests.exceptions.HTTPError as e:
            # Errores HTTP (4xx, 5xx)
            self.logger.error(f"   [ERROR HTTP] Error en {url}: {e}")
        except Exception as e:
            # Cualquier otro error inesperado
            self.logger.error(f"   [ERROR] Excepción inesperada en {url}: {type(e).__name__}: {str(e)}")
            self.logger.debug("Stack trace:", exc_info=True)
            
        return found_ops
    
    # ========================================================================
    # MÉTODO PRIVADO: REALIZAR REQUEST CON RETRY
    # ========================================================================
    @retry_with_backoff(max_retries=3, base_delay=1, max_delay=16)
    def _make_request(self, url: str) -> Optional[requests.Response]:
        """
        Realiza un request HTTP con retry automático.
        
        PARÁMETROS:
            url (str): URL a consultar
        
        RETORNO:
            Response object o None si falla
        
        CARACTERÍSTICAS:
            - Retry automático con backoff exponencial
            - Headers realistas
            - Timeout configurable
            - Raise HTTPError para códigos 4xx/5xx
        """
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout,
                allow_redirects=True
            )
            
            # Raise exception para códigos de error
            response.raise_for_status()
            
            return response
            
        except requests.exceptions.RequestException as e:
            self.logger.debug(f"Request failed: {type(e).__name__}: {str(e)}")
            raise
    
    # ========================================================================
    # MÉTODO PRIVADO: MANEJAR ERRORES HTTP ESPECÍFICOS
    # ========================================================================
    def _handle_http_error(self, status_code: int, url: str) -> None:
        """
        Maneja códigos de error HTTP específicos con mensajes apropiados.
        
        PARÁMETROS:
            status_code (int): Código de estado HTTP
            url (str): URL que generó el error
        """
        error_messages = {
            400: "Solicitud incorrecta (Bad Request)",
            401: "No autorizado - requiere autenticación",
            403: "Acceso prohibido - posible bloqueo",
            404: "Página no encontrada",
            429: "Demasiadas solicitudes - rate limit excedido",
            500: "Error interno del servidor",
            502: "Bad Gateway - servidor no disponible",
            503: "Servicio no disponible temporalmente",
            504: "Gateway Timeout - servidor no responde"
        }
        
        message = error_messages.get(status_code, f"Error HTTP {status_code}")
        
        if status_code >= 500:
            self.logger.error(f"   [ERROR {status_code}] {message} en {url}")
        elif status_code == 429:
            self.logger.warning(f"   [RATE LIMIT] {message} en {url} - Considerar aumentar delay")
        elif status_code in [401, 403]:
            self.logger.warning(f"   [ACCESO DENEGADO {status_code}] {message} en {url}")
        else:
            self.logger.warning(f"   [HTTP {status_code}] {message} en {url}")
