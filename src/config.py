"""
================================================================================
MIA V4.0 - MÓDULO DE CONFIGURACIÓN (config.py)
================================================================================

OBJETIVO GENERAL:
    Centralizar toda la configuración del sistema MIA en un único archivo.
    Define portales a escanear, palabras clave de búsqueda (triggers),
    y configuración de la API de Gemini.

ETAPA: 0 - CONFIGURACIÓN

COMPONENTES PRINCIPALES:

1. CONFIGURACIÓN DE GEMINI AI:
   - GEMINI_MODEL: Modelo de IA a utilizar (gemini-flash-latest)
   - GEMINI_API_KEY: Clave de API cargada desde archivo .env

2. PORTALS (Lista de Portales):
   - Portales de compras públicas a escanear
   - Solo Group 1 está activo (3 portales principales)
   - Otros grupos comentados para etapas futuras
   - Cada portal tiene: name, url, type, search_method, enabled, notes

3. TRIGGERS (Palabras Clave de Oportunidades):
   - Keywords que activan la detección de oportunidades
   - Tipos de licitaciones y contrataciones
   - Términos de proyectos e inversiones
   - Términos de necesidades y tratamientos

4. SEARCH_KEYWORDS (Rubros Específicos):
   - Actualmente solo "agua" está activo
   - Otros rubros comentados para etapas futuras
   - Clasificación en 8 rubros principales (Purificación/Efluentes)

ESTADO ACTUAL (Stage 1):
   - 3 portales activos (Group 1)
   - 18 triggers activos
   - 1 search keyword activo ("agua")
   - Rubros detallados inactivados (comentados)

FUTURAS ETAPAS:
   - Activar más portales (Groups 2-8)
   - Activar búsqueda por rubros específicos
   - Implementar lógica combinada (triggers AND keywords)

AUTOR: Water Tech S.A.
VERSIÓN: 4.0 - Stage 1
================================================================================
"""


import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# CONFIGURACIÓN DE GEMINI AI
# ============================================================================
# GEMINI_MODEL: Modelo de Google Gemini a utilizar para análisis
#               "gemini-flash-latest" es rápido y económico
# GEMINI_API_KEY: Clave de API cargada desde archivo .env
#                 Crear archivo .env con: GEMINI_API_KEY=tu_clave_aqui
# ============================================================================
GEMINI_MODEL = "gemini-flash-latest"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ============================================================================
# CONFIGURACIÓN DEL SISTEMA DE LOGGING
# ============================================================================
# LOG_LEVEL: Nivel de detalle de los logs (DEBUG, INFO, WARNING, ERROR, CRITICAL)
#            DEBUG: Máximo detalle, útil para desarrollo
#            INFO: Información general de operaciones (default)
#            WARNING: Solo advertencias y errores
#            ERROR: Solo errores críticos
# LOG_ROTATION_SIZE_MB: Tamaño máximo de cada archivo de log en MB
# LOG_BACKUP_COUNT: Número de archivos de backup a mantener
# JSON_LOGS: Si es True, los logs se guardan en formato JSON (para integración)
# ============================================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_ROTATION_SIZE_MB = int(os.getenv("LOG_ROTATION_SIZE_MB", "10"))
LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))
JSON_LOGS = os.getenv("JSON_LOGS", "false").lower() == "true"

# ============================================================================
# CONFIGURACIÓN DEL ANALYZER (MEJORAS DE ROBUSTEZ)
# ============================================================================
# GEMINI_RETRY_ATTEMPTS: Número de intentos de retry en caso de error de API
#                        Usa backoff exponencial: 1s, 2s, 4s, etc.
# GEMINI_ENABLE_CACHE: Habilitar caché de respuestas de Gemini (reduce costos)
# GEMINI_CACHE_TTL_HOURS: Tiempo de vida del caché en horas
# GEMINI_COST_PER_1K_TOKENS: Costo aproximado por 1000 tokens (USD)
# GEMINI_METRICS_FILE: Archivo para guardar métricas de uso de API
# ============================================================================
GEMINI_RETRY_ATTEMPTS = int(os.getenv("GEMINI_RETRY_ATTEMPTS", "3"))
GEMINI_ENABLE_CACHE = os.getenv("GEMINI_ENABLE_CACHE", "true").lower() == "true"
GEMINI_CACHE_TTL_HOURS = int(os.getenv("GEMINI_CACHE_TTL_HOURS", "24"))
GEMINI_COST_PER_1K_TOKENS = float(os.getenv("GEMINI_COST_PER_1K_TOKENS", "0.00015"))  # Flash model
GEMINI_METRICS_FILE = os.getenv("GEMINI_METRICS_FILE", "logs/gemini_metrics.json")

# ============================================================================
# PORTALS - LISTA DE PORTALES DE COMPRAS PÚBLICAS
# ============================================================================
# OBJETIVO:
#     Define todos los portales web donde se buscarán oportunidades comerciales
#
# ESTRUCTURA DE CADA PORTAL:
#     - name: Nombre identificador del portal
#     - url: URL completa a escanear
#     - type: Tipo de portal (Detected/Manual/etc.)
#     - search_method: Método de búsqueda (Google Dork/Direct/etc.)
#     - enabled: True para escanear, False para omitir
#     - notes: Notas adicionales sobre el portal
#
# ESTADO ACTUAL (Stage 1):
#     Solo GROUP 1 está activo (3 portales principales de Argentina)
#     Otros grupos están comentados (#) para futuras etapas
#
# GROUP 1 - PORTALES NACIONALES PRINCIPALES:
#     1. comprar.gob.ar - Portal nacional de compras
#     2. contratar.gob.ar - Portal nacional de contrataciones
#     3. boletinoficial.gob.ar - Boletín Oficial (Sección Tercera)
# ============================================================================
PORTALS = [
    # ------------------------------------------------------------------------
    # PORTAL 1: comprar.gob.ar
    # ------------------------------------------------------------------------
    # Portal principal de compras del gobierno nacional argentino
    # ------------------------------------------------------------------------
    {
        "name": "comprar.gob.ar",
        "url": "https://comprar.gob.ar",
        "type": "Detected",
        "search_method": "Google Dork",
        "enabled": True,
        "notes": "Imported from Google Alerts Inventory"
    },
    # ------------------------------------------------------------------------
    # PORTAL 2: contratar.gob.ar
    # ------------------------------------------------------------------------
    # Portal de contrataciones del gobierno nacional
    # ------------------------------------------------------------------------
    {
        "name": "contratar.gob.ar",
        "url": "https://contratar.gob.ar",
        "type": "Detected",
        "search_method": "Google Dork",
        "enabled": True,
        "notes": "Imported from Google Alerts Inventory"
    },
    # ------------------------------------------------------------------------
    # PORTAL 3: boletinoficial.gob.ar
    # ------------------------------------------------------------------------
    # Boletín Oficial - Sección Tercera (Contrataciones Públicas)
    # ------------------------------------------------------------------------
    {
        "name": "boletinoficial.gob.ar",
        "url": "https://www.boletinoficial.gob.ar/seccion/tercera",
        "type": "Detected",
        "search_method": "Google Dork",
        "enabled": True,
        "notes": "Sección Tercera - Contrataciones (Procurement Section)"
    },
    
    # ========================================================================
    # GROUP 2A - FASE 2A: PORTALES CRÍTICOS (4 portales)
    # ========================================================================
    # Portales de máximo valor para el negocio
    # Implementados en Fase 2A - 2026-01-02
    # ========================================================================
    
    # ------------------------------------------------------------------------
    # PORTAL 4: aysa.com.ar
    # ------------------------------------------------------------------------
    # Agua y Saneamientos Argentinos - Empresa de agua más grande
    # PRIORIDAD: ⭐⭐⭐⭐⭐ CRÍTICA
    # VALOR: 🔴 MUY ALTO (100% alineado con el negocio)
    # ------------------------------------------------------------------------
    {
        "name": "aysa.com.ar",
        "url": "https://aysa.com.ar",
        "type": "Empresa Estatal",
        "search_method": "Direct Scraping",
        "enabled": True,
        "use_selenium": False,
        "phase": "2A",
        "priority": 5,
        "notes": "Empresa de agua - 100% relevante para Water Tech"
    },
    
    # ------------------------------------------------------------------------
    # PORTAL 5: opc.gba.gob.ar
    # ------------------------------------------------------------------------
    # Oficina Provincial de Contrataciones - Provincia de Buenos Aires
    # PRIORIDAD: ⭐⭐⭐⭐⭐ CRÍTICA
    # VALOR: 🔴 MUY ALTO (Provincia más grande de Argentina)
    # ------------------------------------------------------------------------
    {
        "name": "opc.gba.gob.ar",
        "url": "https://opc.gba.gob.ar",
        "type": "Portal Provincial",
        "search_method": "Portal Search",
        "enabled": True,
        "use_selenium": False,
        "phase": "2A",
        "priority": 5,
        "notes": "Provincia de Buenos Aires - Alto volumen de licitaciones"
    },
    
    # ------------------------------------------------------------------------
    # PORTAL 6: buenosairescompras.gob.ar
    # ------------------------------------------------------------------------
    # Portal de Compras de la Ciudad Autónoma de Buenos Aires
    # PRIORIDAD: ⭐⭐⭐⭐⭐ CRÍTICA
    # VALOR: 🔴 MUY ALTO (Ciudad de Buenos Aires)
    # ------------------------------------------------------------------------
    {
        "name": "buenosairescompras.gob.ar",
        "url": "https://buenosairescompras.gob.ar",
        "type": "Portal Municipal",
        "search_method": "Category + Search",
        "enabled": True,
        "use_selenium": False,
        "phase": "2A",
        "priority": 5,
        "notes": "Ciudad de Buenos Aires - Gran volumen de licitaciones"
    },
    
    # ------------------------------------------------------------------------
    # PORTAL 7: proveedores.ypf.com
    # ------------------------------------------------------------------------
    # Portal de Proveedores de YPF
    # PRIORIDAD: ⭐⭐⭐⭐⭐ CRÍTICA
    # VALOR: 🔴 MUY ALTO (Grandes proyectos)
    # COMPLEJIDAD: 🔴 Alta (requiere autenticación)
    # ------------------------------------------------------------------------
    {
        "name": "proveedores.ypf.com",
        "url": "https://proveedores.ypf.com",
        "type": "Portal Corporativo",
        "search_method": "Analysis Required",
        "enabled": False,  # Deshabilitado hasta análisis de viabilidad
        "use_selenium": True,
        "phase": "2A",
        "priority": 5,
        "requires_auth": True,
        "notes": "YPF - Requiere análisis de viabilidad (posible autenticación)"
    },
    
    # ========================================================================
    # PORTALES INACTIVADOS (GROUPS 2-8)
    # ========================================================================
    # Los siguientes portales están comentados para etapas futuras
    # Incluyen: portales provinciales, municipales, universitarios,
    # judiciales, organismos descentralizados, empresas estatales,
    # empresas privadas, y plataformas internacionales
    # ========================================================================
    # {
    #     "name": "buenosairescompras.gob.ar",
    #     "url": "https://buenosairescompras.gob.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "opc.gba.gob.ar",
    #     "url": "https://opc.gba.gob.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "compraspublicas.cba.gov.ar",
    #     "url": "https://compraspublicas.cba.gov.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "santafe.gov.ar",
    #     "url": "https://santafe.gov.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "compras.cordoba.gob.ar",
    #     "url": "https://compras.cordoba.gob.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "rosario.gob.ar",
    #     "url": "https://rosario.gob.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "comprar.rionegro.gov.ar",
    #     "url": "https://comprar.rionegro.gov.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "comprar.mendoza.gov.ar",
    #     "url": "https://comprar.mendoza.gov.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "licitaciones.sanjuan.gob.ar",
    #     "url": "https://licitaciones.sanjuan.gob.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "compras.contadurianeuquen.gob.ar",
    #     "url": "https://compras.contadurianeuquen.gob.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "universidadescompran.cin.edu.ar",
    #     "url": "https://universidadescompran.cin.edu.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "uba.ar",
    #     "url": "https://uba.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "conicet.gov.ar",
    #     "url": "https://conicet.gov.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "srpcm.pjn.gov.ar",
    #     "url": "https://srpcm.pjn.gov.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "senado.gob.ar",
    #     "url": "https://senado.gob.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "mpf.gob.ar",
    #     "url": "https://mpf.gob.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "bcra.gob.ar",
    #     "url": "https://bcra.gob.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "pami.org.ar",
    #     "url": "https://pami.org.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "anses.gob.ar",
    #     "url": "https://anses.gob.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "afipcompras.afip.gob.ar",
    #     "url": "https://afipcompras.afip.gob.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "proveedores.ypf.com",
    #     "url": "https://proveedores.ypf.com",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "bna.com.ar",
    #     "url": "https://bna.com.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "eana.com.ar",
    #     "url": "https://eana.com.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "correoargentino.com.ar",
    #     "url": "https://correoargentino.com.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "aysa.com.ar",
    #     "url": "https://aysa.com.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "garrahan.gov.ar",
    #     "url": "https://garrahan.gov.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "compras.inta.gob.ar",
    #     "url": "https://compras.inta.gob.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "service.ariba.com",
    #     "url": "https://service.ariba.com",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "minexus.net",
    #     "url": "https://minexus.net",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "exiros.com",
    #     "url": "https://exiros.com",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "fsp.portal.covisint.com",
    #     "url": "https://fsp.portal.covisint.com",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "samqa.vw.com.ar",
    #     "url": "https://samqa.vw.com.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "esupplierconnect.com",
    #     "url": "https://esupplierconnect.com",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "portalproveedores.acindar.com.ar",
    #     "url": "https://portalproveedores.acindar.com.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "ecup.arcor.com",
    #     "url": "https://ecup.arcor.com",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "compras.lomanegra.com",
    #     "url": "https://compras.lomanegra.com",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "cargill.com",
    #     "url": "https://cargill.com",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "bunge.ar",
    #     "url": "https://bunge.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "proveedores.molinos.com.ar",
    #     "url": "https://proveedores.molinos.com.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "pan-energy.com",
    #     "url": "https://pan-energy.com",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "pampa.com",
    #     "url": "https://pampa.com",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "genneia.com.ar",
    #     "url": "https://genneia.com.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "proveedores.portalcorp.com.ar",
    #     "url": "https://proveedores.portalcorp.com.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "proveedores.poen.com.ar",
    #     "url": "https://proveedores.poen.com.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
    # {
    #     "name": "bagonet.com.ar",
    #     "url": "https://bagonet.com.ar",
    #     "type": "Detected",
    #     "search_method": "Google Dork",
    #     "enabled": True,
    #     "notes": "Imported from Google Alerts Inventory"
    # },
]

# ============================================================================
# TRIGGERS - PALABRAS CLAVE DE OPORTUNIDADES
# ============================================================================
# OBJETIVO:
#     Define las palabras clave que activan la detección de oportunidades
#     Estas son frases que indican que existe una licitación, concurso,
#     proyecto o necesidad de tratamiento
#
# CATEGORÍAS DE TRIGGERS:
#     1. Tipos de Licitaciones (pública, concurso, contratación directa)
#     2. Documentos Técnicos (pliegos, solicitudes)
#     3. Compras y Suministros (equipos, provisión, suministro)
#     4. Proyectos e Inversiones (nuevo proyecto, expansión, inversión)
#     5. Reportes y Necesidades (sostenibilidad, tratamiento)
#
# FUNCIONAMIENTO:
#     Si el scraper encuentra CUALQUIERA de estos triggers en una página,
#     marca esa página como "oportunidad potencial" y la envía al Analyzer
#
# TOTAL: 18 triggers activos
# ============================================================================
TRIGGERS = [
    # ------------------------------------------------------------------------
    # CATEGORÍA 1: TIPOS DE LICITACIONES Y CONTRATACIONES
    # ------------------------------------------------------------------------
    "licitación pública",           # Licitaciones abiertas al público
    "concurso de precios",          # Concursos de precios
    "contratación directa",         # Contrataciones directas sin licitación
    
    # ------------------------------------------------------------------------
    # CATEGORÍA 2: DOCUMENTOS TÉCNICOS
    # ------------------------------------------------------------------------
    "pliego de bases y condiciones",  # Documento con requisitos de licitación
    "pliego licitatorio",             # Pliego de licitación
    "solicitud de cotización",       # Pedidos de cotización
    
    # ------------------------------------------------------------------------
    # CATEGORÍA 3: COMPRAS Y SUMINISTROS
    # ------------------------------------------------------------------------
    "compra de equipos",              # Compra de equipamiento
    "provisión de",                  # Provisión de bienes/servicios
    "suministro de",                  # Suministro de productos
    
    # ------------------------------------------------------------------------
    # CATEGORÍA 4: PROYECTOS E INVERSIONES
    # ------------------------------------------------------------------------
    "nuevo proyecto",                 # Proyectos nuevos
    "expansión de planta",           # Expansiones industriales
    "nueva línea de producción",     # Nuevas líneas productivas
    "inversión ambiental",           # Inversiones en medio ambiente
    "inversión en infraestructura",  # Inversiones en infraestructura
    
    # ------------------------------------------------------------------------
    # CATEGORÍA 5: REPORTES Y NECESIDADES
    # ------------------------------------------------------------------------
    "reporte de sostenibilidad",      # Reportes de sustentabilidad
    "reporte de sustentabilidad",     # Variante de sostenibilidad
    "necesidad de tratamiento"        # Necesidades de tratamiento (agua/efluentes)
]

# ============================================================================
# SEARCH_KEYWORDS - PALABRAS CLAVE DE RUBROS ESPECÍFICOS
# ============================================================================
# OBJETIVO:
#     Define palabras clave específicas de rubros de negocio
#     Actualmente solo "agua" está activo para pruebas iniciales
#
# LÓGICA DE BÚSQUEDA (FUTURO):
#     Oportunidad válida = (Un TRIGGER) AND (Una SEARCH_KEYWORD)
#     Ejemplo: "licitación pública" + "agua" = Oportunidad detectada
#
# ESTADO ACTUAL (Stage 1):
#     Solo se usa "agua" como keyword de prueba
#     La lógica AND aún no está implementada (solo se usan TRIGGERS)
#
# FUTURO:
#     Se activarán keywords específicas por rubro:
#     - Purificación: ósmosis inversa, ultrafiltración, etc.
#     - Efluentes: MBR, DAF, lodos activados, etc.
# ============================================================================
SEARCH_KEYWORDS = [
    "agua"  # Keyword genérica para pruebas iniciales
]

# ============================================================================
# RUBROS - CLASIFICACIÓN DETALLADA POR RUBRO (INACTIVADO)
# ============================================================================
# OBJETIVO:
#     Clasificación detallada de keywords por 8 rubros principales:
#     - Rubro 1: Purificación - Ingeniería
#     - Rubro 2: Purificación - Provisión
#     - Rubro 3: Purificación - Servicios
#     - Rubro 4: Purificación - Gestión Hídrica
#     - Rubro 5: Efluentes - Ingeniería
#     - Rubro 6: Efluentes - Provisión
#     - Rubro 7: Efluentes - Servicios
#     - Rubro 8: Efluentes - Gestión Hídrica
#
# ESTADO ACTUAL:
#     Completamente comentado (#) para Stage 1
#     Se activará en etapas futuras para búsquedas más específicas
#
# CONTENIDO:
#     Cada rubro contiene 30-50 keywords técnicas específicas
#     Ejemplos: "Planta Potabilizadora", "Biorreactor de Membrana", etc.
# ============================================================================
# RUBROS = {
#     "Rubro 1: Purificación - Ingeniería": [
#       "Purificación de Agua (Purificación de Agua Cruda)",
#       "Ingeniería de Detalle",
#       "Estudios de Factibilidad",
#       "Planta Potabilizadora (PTAP)",
#       "Consultoría Hídrica",
#       "Especificaciones Técnicas",
#       "Diseño de Planta",
#       "Agua Ultrapura (UPW)",
#       "Auditoría Hídrica",
#       "Diseño ósmosis inversa",
#       "Ingeniería Básica",
#       "Ingeniería Conceptual",
#       "Ingeniería para Construcción",
#       "FEED (Front-End Engineering Design)",
#       "Relevamiento de plantas",
#       "Propuesta de actualización",
#       "Ingeniería de Proyecto",
#       "Memoria de Cálculo",
#       "Bases de Diseño",
#       "Planos Constructivos",
#       "Dimensionamiento",
#       "Consultoría en tratamiento de agua",
#       "Asesoramiento técnico",
#       "Huella Hídrica",
#       "Eficiencia Hídrica",
#       "Cumplimiento normativo",
#       "Agua de proceso",
#       "Agua para calderas",
#       "Agua desmineralizada",
#       "Agua para inyectables (WFI)",
#       "Diseño de procesos",
#       "Ingeniería Llave en Mano (EPC)",
#       "Análisis de obsolescencia tecnológica",
#       "Diagramas P&ID"
#     ],
#     "Rubro 2: Purificación - Provisión": [
#       "II. Provisión, Agua:",
#       "Ósmosis Inversa Industrial (RO)",
#       "Ultrafiltración (UF)",
#       "Ablandador Industrial",
#       "Filtros de Lecho Profundo (Multimedia)",
#       "Generador de Ozono",
#       "Electrodeionización (EDI)",
#       "Bombas Dosificadoras",
#       "Nanofiltración (NF)",
#       "Sistemas de filtración",
#       "Filtros de Arena",
#       "Filtros de Cartucho",
#       "Filtros de Bolsas",
#       "Filtros Autolimpiantes",
#       "Microfiltración (MF)",
#       "Planta de Ósmosis Inversa",
#       "Skid de RO",
#       "Desalación (Desalinización)",
#       "Módulos de membrana",
#       "Sistemas de intercambio iónico",
#       "Intercambiador Catiónico",
#       "Desmineralizador",
#       "Lecho mixto",
#       "Resinas Selectivas",
#       "Sistema de Cloración",
#       "Dosificación de Hipoclorito de Sodio",
#       "Lámparas UV",
#       "Esterilizador Ultravioleta",
#       "Sistemas de Oxidación Avanzada (AOP)",
#       "Filtros de Carbón Activado",
#       "Medios de Adsorción",
#       "Filtro de Precisión (Multicartucho)",
#       "Plantas contenerizadas",
#       "Dosificadores de Anti-incrustante",
#       "Unidad de Desnitrificación"
#     ],
#     "Rubro 3: Purificación - Servicios": [
#       "III. Servicios e Insumos, Agua:",
#       "Mantenimiento Preventivo",
#       "Revamping",
#       "Resinas de Intercambio Iónico",
#       "Carbón Activado Granular (GAC)",
#       "Membranas de repuesto",
#       "Anti-incrustante (Antiscalant)",
#       "Puesta en Marcha (PEM)",
#       "Servicio de Instalación",
#       "Mantenimiento Correctivo",
#       "Provisión de consumibles",
#       "Provisión de repuestos",
#       "Medios Filtrantes",
#       "Carbón activado en bloque",
#       "Zeolita",
#       "Arena de sílice",
#       "Antracita",
#       "Resinas Catiónicas",
#       "Resinas Aniónicas",
#       "Cartuchos filtrantes",
#       "Bolsas filtrantes",
#       "Floculante",
#       "Coagulante",
#       "Sal para regeneración",
#       "Salmuera",
#       "Diagnóstico de planta",
#       "Limpieza química de membranas (CIP)",
#       "Operación asistida",
#       "Operación y Mantenimiento (O&M)",
#       "Actualización de planta",
#       "Servicio técnico planta",
#       "Alquiler equipos Backup",
#       "Mantenimiento Predictivo",
#       "Provisión de Químicos",
#       "Kits de mantenimiento"
#     ],
#     "Rubro 4: Purificación - Gestión Hídrica": [
#       "IV. Gestión Inteligente, Agua:",
#       "Telemetría",
#       "SCADA",
#       "Monitoreo Remoto",
#       "Sensor de Presión",
#       "Caudalímetro (Medidor de flujo)",
#       "Conductímetro (Medidor de CE)",
#       "Sensor de pH",
#       "Tablero de Control",
#       "Lazos de control",
#       "Optimización de procesos",
#       "Transmisor de presión",
#       "Manómetro",
#       "Sensor de Nivel",
#       "Medidor de Nivel",
#       "Caudalímetro magnético",
#       "Medidor de ORP",
#       "Medidor de TDS",
#       "Turbidímetro",
#       "Sensor de Turbidez",
#       "Analizador de Cloro",
#       "PLC (Controlador Lógico Programable)",
#       "Automatización de planta",
#       "HMI (Human-Machine Interface)",
#       "Internet of Water (IoW)",
#       "Transmisor de nivel ultrasónico",
#       "Medidor de flujo ultrasónico",
#       "Transmisión de datos",
#       "Panel de Control",
#       "Monitoreo a distancia",
#       "Sensor de Temperatura",
#       "Analizador de Iones específicos",
#       "Caudalímetros másicos Coriolis"
#     ],
#     "Rubro 5: Efluentes - Ingeniería": [
#       "Tratamiento de Efluentes (Tratamiento de Efluentes Líquidos)",
#       "V. Ingeniería, Efluentes:",
#       "Planta de Tratamiento de Aguas Residuales (PTAR)",
#       "Reutilización de Efluentes (Reúso de Agua)",
#       "Vertido Cero (ZLD)",
#       "Ingeniería Básica",
#       "Consultoría Ambiental",
#       "Cumplimiento ACUMAR",
#       "Gestión de los Lodos",
#       "Límites de Vuelco",
#       "Ingeniería de Detalle",
#       "Ingeniería Conceptual",
#       "Estudios de Factibilidad",
#       "Especificaciones Técnicas",
#       "Memoria de Cálculo",
#       "Relevamiento de plantas (PTAR)",
#       "Propuestas de actualización",
#       "Estación Depuradora de Aguas Residuales (EDAR)",
#       "Planta de Saneamiento",
#       "Tratamiento de Efluentes",
#       "Aguas residuales",
#       "Tratamiento de lodos",
#       "Deshidratación de Lodos",
#       "Reciclado de efluentes",
#       "Auditoría de vertido",
#       "Estudios de Impacto Ambiental (EIA)",
#       "Diseño de plantas de tratamiento",
#       "Ingeniería de soluciones sobre lodos",
#       "Ingeniería de ZLD (Zero Liquid Discharge)",
#       "Huella Hídrica",
#       "Ingeniería de Proceso",
#       "Planos P&ID detallados",
#       "Diseño llave en mano (EPC)",
#       "Caracterización de efluentes"
#     ],
#     "Rubro 6: Efluentes - Provisión": [
#       "VI. Provisión, Efluentes:",
#       "Biorreactor de Membrana (MBR)",
#       "Flotación por Aire Disuelto (DAF)",
#       "Filtro Prensa",
#       "Sopladores (Blowers)",
#       "Lodos Activados (Barros Activados)",
#       "Reactor Secuencial (SBR)",
#       "Rejas de separación",
#       "Tratamiento de Agua de Producción",
#       "Tamices (rotativo, de tornillo)",
#       "Desarenador",
#       "Desengrasador",
#       "Decantador Lamelar",
#       "Decantador de placas",
#       "Separador API",
#       "Reactor Biológico",
#       "Zanja de Oxidación",
#       "Difusores de Aire",
#       "Reactor de Lecho Móvil (MBBR)",
#       "Reactor UASB",
#       "Espesador de lodos",
#       "Centrífuga (Decanter centrífugo)",
#       "Tornillo deshidratador",
#       "Secado de lodos",
#       "Digestor de lodos",
#       "Tanques Ecualizadores (Homogeneización)",
#       "Mezcladores (Agitadores)",
#       "Floculador",
#       "Plantas Compactas",
#       "Tratamiento terciario",
#       "Filtros cerámicos (Reactores Biológicos Cerámicos)",
#       "Evaporadores MVR (Zero Huella Hídrica)",
#       "Separación líquido sólidos",
#       "Línea de lodos",
#       "Sistemas de Flotación por Aire Disuelto Compactos",
#       "Tanques Contenerizados",
#       "Clarificador de Alta Tasa"
#     ],
#     "Rubro 7: Efluentes - Servicios": [
#       "VII. Servicios e Insumos, Efluentes:",
#       "Operación y Mantenimiento (O&M)",
#       "Polímeros (Polielectrolito)",
#       "Revamping de PTAR",
#       "Floculante",
#       "Coagulante",
#       "Repuestos para Sopladores",
#       "Mantenimiento Planta Efluentes",
#       "Puesta en Marcha de PTAR",
#       "Cloruro férrico",
#       "Antiespumante",
#       "Nutrientes (para biología)",
#       "Repuestos básicos",
#       "Repuesto de Difusores de Aire",
#       "Membranas de MBR (repuesto)",
#       "Instalación de equipos",
#       "Mantenimiento Preventivo",
#       "Mantenimiento Correctivo",
#       "Operación de planta",
#       "Diagnóstico de planta",
#       "Ampliación de PTAR",
#       "Optimización de tratamiento biológico",
#       "Servicio técnico efluentes",
#       "Químicos para efluentes",
#       "Actualización de planta",
#       "Limpieza de difusores",
#       "Limpieza química de membranas (MBR)",
#       "Auditoría de proceso",
#       "Alquiler de plantas de tratamiento",
#       "Operación integral de plantas",
#       "Prolongación de la vida útil",
#       "Biomasa (Inóculo)",
#       "Puesta en funcionamiento",
#       "Provisión de insumos",
#       "Retrofit a MBR"
#     ],
#     "Rubro 8: Efluentes - Gestión Hídrica": [
#       "VIII. Gestión Inteligente, Efluentes:",
#       "Monitoreo de Efluentes",
#       "Medidor de DQO (COD)",
#       "Medidor de DBO (BOD)",
#       "Sensores en línea",
#       "Punto de Control (Efluente)",
#       "Telemetría Efluentes",
#       "Tablero de Control Efluentes",
#       "Medidor de Sólidos Suspendidos (TSS)",
#       "Analizador de TOC",
#       "Sensor de Turbidez (Turbidímetro)",
#       "Sensor de \"Oil in Water\" (Hidrocarburos)",
#       "Medidor de ORP",
#       "Analizador de Amonio",
#       "Analizador de Nitratos",
#       "Analizador de Fosfatos",
#       "Sensor de Presión",
#       "Sensor de Nivel",
#       "Caudalímetro",
#       "Conductímetro (Medidor de CE)",
#       "Medidor de TDS",
#       "Transmisión de datos",
#       "Dashboard de cumplimiento",
#       "SCADA efluentes",
#       "Monitoreo a distancia",
#       "Analizador de Nitrógeno Total",
#       "Analizador de Nitritos",
#       "Monitoreo en tiempo real",
#       "Control en línea (IOW)",
#       "Tableros de control a distancia",
#       "Sensores de calidad de agua",
#       "Monitor en línea",
#       "Sensor MLSS",
#       "Sonda de Oxígeno Disuelto (DO)",
#       "Medidor de pH"
#     ]
# }
