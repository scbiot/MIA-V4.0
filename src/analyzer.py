"""
================================================================================
MIA V4.0 - MÓDULO DE ANÁLISIS CON IA (analyzer.py)
================================================================================

OBJETIVO GENERAL:
    Analizar las oportunidades detectadas por el Scraper utilizando
    Inteligencia Artificial (Google Gemini) para clasificarlas, evaluarlas
    y generar resúmenes técnicos en español.

ETAPA: 2 - ANÁLISIS

FUNCIONAMIENTO:
    1. Carga configuración de API de Gemini desde config.py
    2. Carga plantilla de prompt desde config/prompts.json
    3. Recibe texto de oportunidad + keywords detectadas
    4. Construye prompt personalizado con contexto
    5. Envía a Gemini API para análisis
    6. Parsea respuesta JSON con clasificación y evaluación

ENTRADA:
    - text_content: Texto completo extraído del portal
    - matched_keywords: Lista de triggers que activaron la detección

SALIDA (JSON):
    - MIA_Rubro: Clasificación en categorías (Purificación/Efluentes)
    - MIA_Score_IA: Relevancia de 0-100
    - MIA_Resumen_Tecnico: Resumen en español (max 300 palabras)
    - MIA_Link_al_Pliego: URL del pliego si se encuentra
    - MIA_Empresa_Asignada: Sugerencia de empresa (Water Tech/Eco Tech)
    - MIA_Preguntas_Tecnicas: Preguntas para evaluar la oportunidad

CONFIGURACIÓN REQUERIDA:
    - .env: GEMINI_API_KEY (clave de API de Google)
    - config.py: GEMINI_MODEL (modelo a utilizar)
    - config/prompts.json: Plantilla de prompt en español

DEPENDENCIAS:
    - google.generativeai: SDK de Google Gemini
    - python-dotenv: Carga de variables de entorno

AUTOR: Water Tech S.A.
VERSIÓN: 4.0 - Stage 1
================================================================================
"""

import google.generativeai as genai
import os
import json
import logging
import time
import hashlib
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# CLASE ANALYZER - MOTOR DE ANÁLISIS CON INTELIGENCIA ARTIFICIAL
# ============================================================================
class Analyzer:
    """
    Clase responsable de analizar oportunidades usando Google Gemini AI.
    
    RESPONSABILIDADES:
        - Configurar conexión con Gemini API
        - Cargar plantillas de prompts desde configuración
        - Enviar oportunidades a Gemini para análisis
        - Parsear y validar respuestas JSON
        - Manejar errores de API y formato
    """
    
    def __init__(self):
        """
        CONSTRUCTOR - Inicialización del Analyzer
        
        ACCIONES:
            1. Configura logger para registro de operaciones
            2. Carga API key desde config.py (que la lee de .env)
            3. Configura cliente de Gemini API
            4. Carga plantilla de prompt desde config/prompts.json
            5. Carga configuración de retry attempts
        
        VALIDACIÓN:
            Si no hay API key, registra warning pero no falla
            (permite testing sin credenciales)
        """
        self.logger = logging.getLogger(__name__)
        from src.config import (
            GEMINI_API_KEY, GEMINI_MODEL, GEMINI_RETRY_ATTEMPTS,
            GEMINI_ENABLE_CACHE, GEMINI_CACHE_TTL_HOURS,
            GEMINI_COST_PER_1K_TOKENS, GEMINI_METRICS_FILE
        )
        
        self.api_key = GEMINI_API_KEY
        self.retry_attempts = GEMINI_RETRY_ATTEMPTS
        self.enable_cache = GEMINI_ENABLE_CACHE
        self.cache_ttl_hours = GEMINI_CACHE_TTL_HOURS
        self.cost_per_1k_tokens = GEMINI_COST_PER_1K_TOKENS
        self.metrics_file = GEMINI_METRICS_FILE
        
        # Inicializar caché en memoria
        self.cache = {}  # {hash: {"response": data, "timestamp": datetime, "tokens": int}}
        
        # Inicializar métricas
        self.metrics = {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "total_tokens": 0,
            "total_cost_usd": 0.0,
            "requests_by_date": {}
        }
        self._load_metrics()
        
        if self.api_key:
            # Configurar cliente de Gemini con la API key
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(GEMINI_MODEL)
        else:
            self.logger.warning("GEMINI_API_KEY not found in .env. Analyzer will fail or mock.")
        
        # Cargar plantilla de prompt desde archivo JSON
        self.prompt_template = self._load_prompt_template()

    # ========================================================================
    # MÉTODO PRIVADO: CARGAR PLANTILLA DE PROMPT
    # ========================================================================
    def _load_prompt_template(self):
        """
        Carga la plantilla de prompt desde config/prompts.json
        
        OBJETIVO:
            Externalizar el prompt de Gemini en un archivo JSON para
            facilitar modificaciones sin tocar el código Python
        
        ESTRUCTURA DEL JSON:
            {
                "analysis_prompt": {
                    "template": "Texto del prompt con {placeholders}",
                    "variables": {...}
                }
            }
        
        RETORNO:
            String con la plantilla de prompt (con placeholders {variable})
        
        FALLBACK:
            Si falla la carga, retorna un prompt básico en español
        """
        try:
            # Construir ruta al archivo prompts.json
            prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'prompts.json')
            with open(prompt_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config['analysis_prompt']['template']
        except Exception as e:
            self.logger.error(f"Error loading prompt template: {e}")
            # Fallback: Prompt básico si no se puede cargar el archivo
            return """Analiza el siguiente texto y extrae información en formato JSON con los campos:
MIA_Rubro, MIA_Score_IA, MIA_Link_al_Pliego, MIA_Resumen_Tecnico, MIA_Empresa_Asignada, MIA_Preguntas_Tecnicas.
Responde en castellano.

Texto: {text_content}"""

    # ========================================================================
    # MÉTODOS DE CACHÉ Y MÉTRICAS
    # ========================================================================
    
    def _generate_cache_key(self, text_content):
        """
        Genera una clave de caché única basada en el contenido del texto.
        
        OBJETIVO:
            Crear un hash único para cada texto analizado, permitiendo
            detectar textos duplicados y reutilizar análisis previos
        
        PARÁMETROS:
            text_content (str): Texto a analizar
        
        RETORNO:
            String con hash SHA-256 del texto (primeros 16 caracteres)
        """
        # Normalizar texto (minúsculas, sin espacios extra)
        normalized = text_content.lower().strip()
        # Generar hash SHA-256
        hash_object = hashlib.sha256(normalized.encode('utf-8'))
        # Retornar primeros 16 caracteres del hash
        return hash_object.hexdigest()[:16]
    
    def _check_cache(self, cache_key):
        """
        Verifica si existe una respuesta en caché y si aún es válida.
        
        OBJETIVO:
            Evitar llamadas redundantes a Gemini API reutilizando
            análisis previos de textos idénticos
        
        PARÁMETROS:
            cache_key (str): Clave de caché generada por _generate_cache_key
        
        RETORNO:
            Diccionario con análisis si está en caché y es válido, None si no
        """
        if not self.enable_cache:
            return None
        
        if cache_key not in self.cache:
            return None
        
        cached_item = self.cache[cache_key]
        
        # Verificar si el caché ha expirado
        cache_age = datetime.now() - cached_item["timestamp"]
        if cache_age > timedelta(hours=self.cache_ttl_hours):
            # Caché expirado, eliminarlo
            del self.cache[cache_key]
            self.logger.debug(f"Caché expirado para key: {cache_key}")
            return None
        
        # Caché válido
        self.logger.info(f"Cache HIT para key: {cache_key} (edad: {cache_age})")
        return cached_item["response"]
    
    def _save_to_cache(self, cache_key, response_data, tokens_used):
        """
        Guarda una respuesta de Gemini en el caché.
        
        PARÁMETROS:
            cache_key (str): Clave de caché
            response_data (dict): Respuesta de Gemini
            tokens_used (int): Número de tokens utilizados
        """
        if not self.enable_cache:
            return
        
        self.cache[cache_key] = {
            "response": response_data,
            "timestamp": datetime.now(),
            "tokens": tokens_used
        }
        self.logger.debug(f"Guardado en caché: {cache_key}")
    
    def _load_metrics(self):
        """
        Carga métricas de uso de API desde archivo JSON.
        
        OBJETIVO:
            Mantener un registro persistente del uso de Gemini API
            para tracking de costos y optimización
        """
        try:
            if os.path.exists(self.metrics_file):
                with open(self.metrics_file, 'r', encoding='utf-8') as f:
                    loaded_metrics = json.load(f)
                    # Actualizar métricas con datos cargados
                    self.metrics.update(loaded_metrics)
                    self.logger.debug(f"Métricas cargadas: {self.metrics['total_requests']} requests")
        except Exception as e:
            self.logger.warning(f"No se pudieron cargar métricas: {e}")
    
    def _save_metrics(self):
        """
        Guarda métricas de uso de API en archivo JSON.
        """
        try:
            # Crear directorio logs/ si no existe
            os.makedirs(os.path.dirname(self.metrics_file), exist_ok=True)
            
            with open(self.metrics_file, 'w', encoding='utf-8') as f:
                json.dump(self.metrics, f, indent=2, ensure_ascii=False)
                self.logger.debug("Métricas guardadas")
        except Exception as e:
            self.logger.error(f"Error guardando métricas: {e}")
    
    def _estimate_tokens(self, text):
        """
        Estima el número de tokens en un texto.
        
        OBJETIVO:
            Aproximar el número de tokens para calcular costos
            Regla aproximada: 1 token ≈ 4 caracteres en español
        
        PARÁMETROS:
            text (str): Texto a estimar
        
        RETORNO:
            int: Número estimado de tokens
        """
        # Estimación: 1 token ≈ 4 caracteres
        return len(text) // 4
    
    def _update_metrics(self, tokens_used, from_cache=False):
        """
        Actualiza métricas de uso de API.
        
        PARÁMETROS:
            tokens_used (int): Número de tokens utilizados
            from_cache (bool): Si la respuesta vino del caché
        """
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Actualizar contadores generales
        self.metrics["total_requests"] += 1
        
        if from_cache:
            self.metrics["cache_hits"] += 1
        else:
            self.metrics["cache_misses"] += 1
            self.metrics["total_tokens"] += tokens_used
            
            # Calcular costo
            cost = (tokens_used / 1000) * self.cost_per_1k_tokens
            self.metrics["total_cost_usd"] += cost
        
        # Actualizar métricas por fecha
        if today not in self.metrics["requests_by_date"]:
            self.metrics["requests_by_date"][today] = {
                "requests": 0,
                "cache_hits": 0,
                "tokens": 0,
                "cost_usd": 0.0
            }
        
        self.metrics["requests_by_date"][today]["requests"] += 1
        
        if from_cache:
            self.metrics["requests_by_date"][today]["cache_hits"] += 1
        else:
            self.metrics["requests_by_date"][today]["tokens"] += tokens_used
            cost = (tokens_used / 1000) * self.cost_per_1k_tokens
            self.metrics["requests_by_date"][today]["cost_usd"] += cost
        
        # Guardar métricas
        self._save_metrics()
        
        # Log de métricas
        cache_rate = (self.metrics["cache_hits"] / self.metrics["total_requests"] * 100) if self.metrics["total_requests"] > 0 else 0
        self.logger.info(f"Métricas API - Total: {self.metrics['total_requests']} | "
                        f"Cache: {cache_rate:.1f}% | "
                        f"Tokens: {self.metrics['total_tokens']} | "
                        f"Costo: ${self.metrics['total_cost_usd']:.4f}")

    # ========================================================================
    # MÉTODO PRIVADO: VALIDAR RESPUESTA DE ANÁLISIS
    # ========================================================================
    def _validate_analysis_response(self, response_data):
        """
        Valida que la respuesta de Gemini tenga la estructura correcta.
        
        OBJETIVO:
            Asegurar que Gemini retornó todos los campos requeridos
            con los tipos de datos correctos
        
        CAMPOS REQUERIDOS:
            - MIA_Rubro: string (clasificación)
            - MIA_Score_IA: int 0-100 (relevancia)
            - MIA_Resumen_Tecnico: string (resumen)
        
        CAMPOS OPCIONALES:
            - MIA_Link_al_Pliego: string (URL)
            - MIA_Empresa_Asignada: string (Water Tech/Eco Tech)
            - MIA_Preguntas_Tecnicas: string o list
        
        RETORNO:
            True si la validación es exitosa, False si falla
        """
        if not isinstance(response_data, dict):
            self.logger.error("Respuesta no es un diccionario JSON válido")
            return False
        
        # Validar campos requeridos
        required_fields = ['MIA_Rubro', 'MIA_Score_IA', 'MIA_Resumen_Tecnico']
        for field in required_fields:
            if field not in response_data:
                self.logger.error(f"Campo requerido faltante: {field}")
                return False
        
        # Validar tipo de datos de MIA_Score_IA
        score = response_data.get('MIA_Score_IA')
        if not isinstance(score, (int, float)):
            self.logger.error(f"MIA_Score_IA debe ser numérico, recibido: {type(score)}")
            return False
        
        # Validar rango de score (0-100)
        if not (0 <= score <= 100):
            self.logger.warning(f"MIA_Score_IA fuera de rango (0-100): {score}")
            # No falla la validación, solo advierte
        
        # Validar que campos de texto no estén vacíos
        if not response_data.get('MIA_Rubro', '').strip():
            self.logger.error("MIA_Rubro está vacío")
            return False
        
        if not response_data.get('MIA_Resumen_Tecnico', '').strip():
            self.logger.error("MIA_Resumen_Tecnico está vacío")
            return False
        
        # Advertir sobre campos opcionales faltantes (no falla validación)
        optional_fields = ['MIA_Link_al_Pliego', 'MIA_Empresa_Asignada', 'MIA_Preguntas_Tecnicas']
        for field in optional_fields:
            if field not in response_data:
                self.logger.debug(f"Campo opcional faltante: {field}")
        
        return True

    # ========================================================================
    # MÉTODO PRIVADO: RETRY CON BACKOFF EXPONENCIAL
    # ========================================================================
    def _retry_with_backoff(self, func, *args, **kwargs):
        """
        Ejecuta una función con retry y backoff exponencial.
        
        OBJETIVO:
            Manejar errores transitorios de API (rate limit, network errors)
            con reintentos inteligentes
        
        ESTRATEGIA:
            - Intento 1: Inmediato
            - Intento 2: Espera 1 segundo
            - Intento 3: Espera 2 segundos
            - Intento 4: Espera 4 segundos
            - etc. (backoff exponencial: 2^(attempt-1))
        
        PARÁMETROS:
            func: Función a ejecutar
            *args, **kwargs: Argumentos para la función
        
        RETORNO:
            Resultado de la función si tiene éxito, None si todos los intentos fallan
        """
        for attempt in range(1, self.retry_attempts + 1):
            try:
                # Intentar ejecutar la función
                return func(*args, **kwargs)
            
            except Exception as e:
                error_msg = str(e).lower()
                
                # Detectar tipos específicos de errores
                is_rate_limit = 'rate limit' in error_msg or 'quota' in error_msg
                is_network = 'connection' in error_msg or 'timeout' in error_msg
                is_api_error = 'api' in error_msg or '429' in error_msg or '503' in error_msg
                
                # Si es el último intento, no reintentar
                if attempt == self.retry_attempts:
                    self.logger.error(f"Fallo después de {self.retry_attempts} intentos: {e}")
                    return None
                
                # Calcular tiempo de espera (backoff exponencial)
                wait_time = 2 ** (attempt - 1)  # 1s, 2s, 4s, 8s...
                
                # Log del reintento
                if is_rate_limit:
                    self.logger.warning(f"Rate limit detectado. Reintentando en {wait_time}s (intento {attempt}/{self.retry_attempts})")
                elif is_network:
                    self.logger.warning(f"Error de red. Reintentando en {wait_time}s (intento {attempt}/{self.retry_attempts})")
                elif is_api_error:
                    self.logger.warning(f"Error de API. Reintentando en {wait_time}s (intento {attempt}/{self.retry_attempts})")
                else:
                    self.logger.warning(f"Error: {e}. Reintentando en {wait_time}s (intento {attempt}/{self.retry_attempts})")
                
                # Esperar antes del siguiente intento
                time.sleep(wait_time)
        
        return None


    # ========================================================================
    # MÉTODO PRINCIPAL: ANALIZAR OPORTUNIDAD CON IA
    # ========================================================================
    def analyze_opportunity(self, text_content, matched_keywords=None):
        """
        Analiza una oportunidad usando Gemini AI.
        
        PARÁMETROS:
            text_content (str): Texto completo de la oportunidad
            matched_keywords (list): Lista de triggers detectados
        
        PROCESO:
            1. Valida que exista API key
            2. Formatea las keywords para el prompt
            3. Construye prompt usando la plantilla
            4. Envía a Gemini API con retry automático
            5. Limpia y parsea respuesta JSON
            6. Valida estructura de la respuesta
        
        MEJORAS IMPLEMENTADAS (Fase 1):
            - Retry con backoff exponencial para errores de API
            - Validación de estructura JSON de respuesta
            - Mejor manejo de errores con logging detallado
        
        RETORNO:
            Diccionario con análisis (si éxito) o None (si error)
        """
        if not self.api_key:
            self.logger.error("Cannot analyze: No API Key.")
            return None

        # --------------------------------------------------------------------
        # VERIFICAR CACHÉ
        # --------------------------------------------------------------------
        # Generar clave de caché basada en el contenido
        # --------------------------------------------------------------------
        cache_key = self._generate_cache_key(text_content)
        
        # Verificar si existe en caché
        cached_response = self._check_cache(cache_key)
        if cached_response is not None:
            # Respuesta encontrada en caché
            tokens_estimated = self._estimate_tokens(text_content)
            self._update_metrics(tokens_estimated, from_cache=True)
            return cached_response

        # --------------------------------------------------------------------
        # PREPARACIÓN DEL PROMPT
        # --------------------------------------------------------------------
        # Convierte lista de keywords en string para incluir en el prompt
        # --------------------------------------------------------------------
        keywords_str = ", ".join(matched_keywords) if matched_keywords else "N/A"
        
        # Construir prompt usando plantilla con variables
        truncated_text = text_content[:10000]  # Truncar a 10k caracteres
        prompt = self.prompt_template.format(
            matched_keywords=keywords_str,
            text_content=truncated_text
        )
        
        # Estimar tokens para métricas
        tokens_estimated = self._estimate_tokens(prompt + truncated_text)
        
        # --------------------------------------------------------------------
        # FUNCIÓN INTERNA PARA LLAMADA A GEMINI
        # --------------------------------------------------------------------
        # Esta función se ejecutará con retry automático
        # --------------------------------------------------------------------
        def call_gemini_api():
            """Función interna para llamar a Gemini API"""
            response = self.model.generate_content(prompt)
            
            # Limpiar respuesta (remover markdown ```json```)
            text = response.text.replace("```json", "").replace("```", "").strip()
            
            if not text:
                raise ValueError("Gemini returned empty response")
            
            # Parsear JSON
            return json.loads(text)
        
        # --------------------------------------------------------------------
        # LLAMADA A GEMINI CON RETRY AUTOMÁTICO
        # --------------------------------------------------------------------
        try:
            # Usar retry_with_backoff para manejar errores transitorios
            analysis_data = self._retry_with_backoff(call_gemini_api)
            
            if analysis_data is None:
                self.logger.error("Gemini API call failed after all retry attempts")
                # Actualizar métricas de fallo
                self._update_metrics(tokens_estimated, from_cache=False)
                return None
            
            # ----------------------------------------------------------------
            # VALIDACIÓN DE RESPUESTA
            # ----------------------------------------------------------------
            if not self._validate_analysis_response(analysis_data):
                self.logger.error("Gemini response failed validation")
                self.logger.debug(f"Invalid response: {json.dumps(analysis_data, indent=2)}")
                # Actualizar métricas de fallo
                self._update_metrics(tokens_estimated, from_cache=False)
                return None
            
            # ----------------------------------------------------------------
            # GUARDAR EN CACHÉ Y ACTUALIZAR MÉTRICAS
            # ----------------------------------------------------------------
            self._save_to_cache(cache_key, analysis_data, tokens_estimated)
            self._update_metrics(tokens_estimated, from_cache=False)
            
            # Respuesta válida
            self.logger.debug(f"Analysis successful: {analysis_data.get('MIA_Rubro')} - Score: {analysis_data.get('MIA_Score_IA')}")
            return analysis_data
            
        # ====================================================================
        # MANEJO DE ERRORES
        # ====================================================================
        except json.JSONDecodeError as e:
            # Error: Gemini no retornó JSON válido
            self.logger.error(f"Gemini response is not valid JSON: {e}")
            self._update_metrics(tokens_estimated, from_cache=False)
            return None
        except Exception as e:
            # Cualquier otro error no manejado
            self.logger.error(f"Unexpected error in analysis: {e}")
            self._update_metrics(tokens_estimated, from_cache=False)
            return None
