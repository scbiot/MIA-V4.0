"""
================================================================================
MIA V4.0 - MÓDULO PRINCIPAL (main.py)
================================================================================

OBJETIVO GENERAL:
    Este es el punto de entrada principal del sistema MIA (Monitor de 
    Inteligencia de Adquisiciones) versión 4.0. Coordina el flujo completo
    de detección y análisis de oportunidades comerciales en portales públicos.

ETAPAS DEL PROCESO:
    ETAPA 0 (Configuración): Carga de configuración desde src/config.py
    ETAPA 1 (Scraping): Búsqueda de oportunidades en portales web
    ETAPA 2 (Análisis): Evaluación con IA (Gemini) de cada oportunidad
    ETAPA 3 (Almacenamiento): Guardado de resultados en CSV/Google Sheets

COMPONENTES PRINCIPALES:
    - Scraper: Busca keywords en portales de compras públicas
    - Analyzer: Analiza con IA Gemini la relevancia de cada oportunidad
    - SheetsManager: Gestiona la salida de datos (CSV y Google Sheets)

FLUJO DE EJECUCIÓN:
    1. Inicialización de componentes
    2. Scraping de portales activos (Group 1)
    3. Análisis con IA de cada oportunidad detectada
    4. Almacenamiento de resultados en results_stage1.csv
    5. Registro de ejecución en historial_ejecuciones.txt

ARCHIVOS DE SALIDA:
    - results_stage1.csv: Resultados del análisis
    - historial_ejecuciones.txt: Log detallado de cada ejecución

AUTOR: Water Tech S.A.
VERSIÓN: 4.0 - Stage 1
================================================================================
"""

import logging
import logging.config
from src.scraper import Scraper
from src.analyzer import Analyzer
from src.sheets_manager import SheetsManager

# ============================================================================
# CONFIGURACIÓN DEL SISTEMA DE LOGGING
# ============================================================================
# OBJETIVO: Registrar todas las operaciones del sistema tanto en consola
#           como en archivo para trazabilidad y debugging
# 
# MEJORAS IMPLEMENTADAS (Fase 1):
#   - Niveles de log configurables desde .env (DEBUG/INFO/WARNING/ERROR)
#   - Rotación automática de archivos por tamaño
#   - Logs organizados en directorio logs/
#   - Mantiene últimos N archivos de backup
# ============================================================================

import os
from logging.handlers import RotatingFileHandler

# Importar configuración de logging desde config.py
from src.config import LOG_LEVEL, LOG_ROTATION_SIZE_MB, LOG_BACKUP_COUNT

# Crear directorio logs/ si no existe
os.makedirs('logs', exist_ok=True)

# ----------------------------------------------------------------------------
# CONFIGURACIÓN DEL LOGGER ROOT
# ----------------------------------------------------------------------------
# Crear logger root y configurar nivel desde .env
# ----------------------------------------------------------------------------
logger = logging.getLogger()

# Convertir nivel de string a constante de logging
level_map = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}
logger.setLevel(level_map.get(LOG_LEVEL, logging.INFO))

# ----------------------------------------------------------------------------
# HANDLERS DE LOGGING
# ----------------------------------------------------------------------------
# c_handler: Muestra mensajes en consola (para monitoreo en tiempo real)
# f_handler: Guarda mensajes en archivo con rotación automática
# ----------------------------------------------------------------------------
c_handler = logging.StreamHandler()

# RotatingFileHandler: Rota archivos automáticamente cuando alcanzan el tamaño límite
# maxBytes: Tamaño máximo en bytes (convertir MB a bytes)
# backupCount: Número de archivos de backup a mantener
f_handler = RotatingFileHandler(
    'logs/main.log',
    mode='a',
    maxBytes=LOG_ROTATION_SIZE_MB * 1024 * 1024,  # Convertir MB a bytes
    backupCount=LOG_BACKUP_COUNT,
    encoding='utf-8'
)

# Aplicar el nivel configurado a ambos handlers
c_handler.setLevel(level_map.get(LOG_LEVEL, logging.INFO))
f_handler.setLevel(level_map.get(LOG_LEVEL, logging.INFO))

# ----------------------------------------------------------------------------
# FORMATO DE MENSAJES DE LOG
# ----------------------------------------------------------------------------
# Formato: [Fecha/Hora] - [Nivel] - [Mensaje]
# Ejemplo: 2025-12-11 08:45:19 - INFO - Inicio de ejecución
# ----------------------------------------------------------------------------
log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
c_handler.setFormatter(log_format)
f_handler.setFormatter(log_format)

# ----------------------------------------------------------------------------
# REGISTRO DE HANDLERS
# ----------------------------------------------------------------------------
# Evita duplicación de handlers si el módulo se importa múltiples veces
# ----------------------------------------------------------------------------
if not logger.handlers:
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

# Log inicial indicando nivel configurado
logger.info(f"Sistema de logging inicializado - Nivel: {LOG_LEVEL}")

# ============================================================================
# FUNCIÓN PRINCIPAL - ORQUESTADOR DEL SISTEMA
# ============================================================================
def main():
    """
    OBJETIVO:
        Coordina la ejecución completa del sistema MIA en 3 pasos:
        1. SCRAPING: Búsqueda de oportunidades en portales
        2. ANÁLISIS: Evaluación con IA de cada oportunidad
        3. ALMACENAMIENTO: Guardado de resultados
    
    MANEJO DE ERRORES:
        - Try/Except captura cualquier error crítico
        - Finally asegura que el programa espere antes de cerrar
    """
    try:
        logger.info("="*50)
        logger.info("INICIO DE EJECUCION MIA V4.0 Stage 1")
        logger.info("="*50)
        
        # ------------------------------------------------------------------------
        # PASO 0: INICIALIZACIÓN DE COMPONENTES
        # ------------------------------------------------------------------------
        # Crea instancias de los 3 módulos principales del sistema
        # ------------------------------------------------------------------------
        logger.info("Inicializando componentes...")
        scraper = Scraper()      # Módulo de búsqueda web
        analyzer = Analyzer()    # Módulo de análisis con IA
        sheets = SheetsManager()  # Módulo de salida de datos
        
        # ------------------------------------------------------------------------
        # PASO 1: SCRAPING DE PORTALES
        # ------------------------------------------------------------------------
        # OBJETIVO: Buscar en todos los portales activos (Group 1) las palabras
        #           clave definidas en TRIGGERS (config.py)
        # SALIDA: Lista de oportunidades detectadas con sus URLs y keywords
        # ------------------------------------------------------------------------
        logger.info("\n>>> PASO 1: Scraping de Portales")
        raw_ops = scraper.search_all()
        logger.info(f"Se encontraron {len(raw_ops)} oportunidades potenciales.")
        
        # ------------------------------------------------------------------------
        # PASO 2: ANÁLISIS CON INTELIGENCIA ARTIFICIAL
        # ------------------------------------------------------------------------
        # OBJETIVO: Evaluar cada oportunidad detectada usando Gemini AI para:
        #           - Clasificar en rubros (Purificación/Efluentes)
        #           - Asignar score de relevancia (0-100)
        #           - Generar resumen técnico en español
        # ENTRADA: Texto completo de cada oportunidad + keywords detectadas
        # SALIDA: Análisis estructurado en formato JSON
        # ------------------------------------------------------------------------
        logger.info("\n>>> PASO 2: Análisis con Gemini")
        if not raw_ops:
            logger.info("No hay oportunidades para analizar.")
        
        for op in raw_ops:
            logger.info(f"Analizando oportunidad: {op['url']}")
            analysis = analyzer.analyze_opportunity(
                op['full_text'],
                matched_keywords=op.get('matched_keywords', [])
            )
            
            if analysis:
                # --------------------------------------------------------------------
                # COMBINACIÓN DE DATOS: Scraping + Análisis IA
                # --------------------------------------------------------------------
                # Fusiona la información del scraping (portal, URL, keywords)
                # con el análisis de Gemini (rubro, score, resumen)
                # --------------------------------------------------------------------
                row_data = {
                    "Portal": op['portal'],                                              # Origen de la oportunidad
                    "MIA_URL": op['url'],                                                # Link directo
                    "MIA_Keywords_Detectadas": ", ".join(op.get('matched_keywords', [])), # Triggers encontrados
                    "MIA_Rubro": analysis.get("MIA_Rubro"),                             # Clasificación IA
                    "MIA_Score_IA": analysis.get("MIA_Score_IA"),                       # Relevancia 0-100
                    "MIA_Resumen_Tecnico": analysis.get("MIA_Resumen_Tecnico")          # Resumen en español
                }
                
                logger.info(f"Oportunidad Analizada: {row_data['MIA_Rubro']} - Score: {row_data['MIA_Score_IA']}")
                
                # --------------------------------------------------------------------
                # PASO 3: ALMACENAMIENTO DE RESULTADOS
                # --------------------------------------------------------------------
                # Guarda cada oportunidad analizada en results_stage1.csv
                # --------------------------------------------------------------------
                sheets.add_row(row_data)
        
        logger.info("\n>>> PROCESO COMPLETADO EXITOSAMENTE. Verifique results_stage1.csv")

    # ========================================================================
    # MANEJO DE ERRORES Y FINALIZACIÓN
    # ========================================================================
    except Exception as e:
        # Captura cualquier error no previsto y lo registra con stack trace completo
        logger.exception("OCURRIO UN ERROR CRITICO DURANTE LA EJECUCION:")
    finally:
        # Asegura que el programa no se cierre automáticamente para permitir
        # al usuario revisar los mensajes en consola
        logger.info("="*50)
        print("\nPresione ENTER para salir...")
        input()

# ============================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================================
# Esta condición asegura que main() solo se ejecute cuando se corre
# directamente este archivo, no cuando se importa como módulo
# ============================================================================
if __name__ == "__main__":
    main()
