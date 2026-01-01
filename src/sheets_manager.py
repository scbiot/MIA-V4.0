"""
================================================================================
MIA V4.0 - MÓDULO DE GESTIÓN DE SALIDA (sheets_manager.py)
================================================================================

OBJETIVO GENERAL:
    Gestionar la salida de resultados del sistema MIA, guardando las
    oportunidades analizadas en archivos CSV y (futuro) Google Sheets.

ETAPA: 3 - ALMACENAMIENTO

FUNCIONAMIENTO:
    1. Recibe datos de oportunidades analizadas (dict)
    2. Valida datos antes de escribir
    3. Detecta y evita duplicados
    4. Crea backups automáticos
    5. Agrega timestamps y metadata
    6. Escribe cada oportunidad como una fila en results_stage1.csv

SALIDA ACTUAL (Stage 1):
    - Archivo: results_stage1.csv (configurable desde .env)
    - Formato: CSV con encoding UTF-8
    - Columnas:
        * Timestamp_Deteccion: Fecha y hora de detección
        * Portal: Nombre del portal donde se detectó
        * MIA_URL: URL de la oportunidad
        * MIA_Keywords_Detectadas: Triggers encontrados
        * MIA_Rubro: Clasificación por rubro
        * MIA_Score_IA: Score de relevancia (0-100)
        * MIA_Resumen_Tecnico: Resumen en español

MEJORAS FASE 1:
    - ✅ Validación de datos antes de escribir
    - ✅ Detección de duplicados por URL
    - ✅ Backup automático antes de cada ejecución
    - ✅ Timestamps automáticos
    - ✅ Configuración desde variables de entorno

FUTURAS FUNCIONALIDADES:
    - Integración con Google Sheets API
    - Sincronización automática con spreadsheet
    - Notificaciones por email
    - Dashboard en tiempo real

DEPENDENCIAS:
    - csv: Manejo de archivos CSV
    - os: Verificación de existencia de archivos
    - shutil: Copia de archivos para backup
    - datetime: Timestamps
    - typing: Type hints

AUTOR: Water Tech S.A.
VERSIÓN: 4.0 - Stage 1 + Fase 1 Mejoras
================================================================================
"""

import logging
import json
import csv
import os
import shutil
from datetime import datetime
from typing import Dict, Any, Set
from urllib.parse import urlparse

# ============================================================================
# CLASE SHEETSMANAGER - GESTOR DE SALIDA DE DATOS
# ============================================================================
class SheetsManager:
    """
    Clase responsable de guardar resultados del análisis.
    
    RESPONSABILIDADES:
        - Validar datos antes de escribir
        - Detectar y evitar duplicados
        - Crear backups automáticos
        - Escribir resultados en archivo CSV
        - Agregar timestamps y metadata
        - (Futuro) Sincronizar con Google Sheets
        - Manejar encoding UTF-8 para caracteres especiales
    """
    
    def __init__(self, key_path="data/service_account.json"):
        """
        CONSTRUCTOR - Inicialización del SheetsManager
        
        PARÁMETROS:
            key_path (str): Ruta al archivo de credenciales de Google Sheets
                           (actualmente no se usa, preparado para futuro)
        
        ACCIONES:
            1. Configura logger para registro de operaciones
            2. Verifica existencia de credenciales de Google Sheets
            3. Carga configuración desde variables de entorno
            4. Inicializa conjunto de URLs procesadas
            5. Crea directorio de backups si no existe
            6. Carga URLs ya procesadas del CSV existente
        
        ESTADO ACTUAL:
            Solo modo CSV (Google Sheets no implementado)
        """
        self.logger = logging.getLogger(__name__)
        self.key_path = key_path
        self.has_creds = os.path.exists(key_path)
        if not self.has_creds:
            self.logger.warning(f"Service account file not found at {key_path}. Outputting to CSV only.")
        
        # Configuración desde variables de entorno
        self.output_file = os.getenv('OUTPUT_CSV_FILE', 'results_stage1.csv')
        self.create_backup = os.getenv('OUTPUT_CREATE_BACKUP', 'true').lower() == 'true'
        self.backup_dir = os.getenv('OUTPUT_BACKUP_DIR', 'backups')
        
        # Conjunto para tracking de URLs procesadas (evitar duplicados)
        self.processed_urls: Set[str] = set()
        
        # Crear directorio de backups si no existe
        if self.create_backup and not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
            self.logger.info(f"Directorio de backups creado: {self.backup_dir}")
        
        # Cargar URLs ya procesadas si el archivo existe
        self._load_processed_urls()
        
        self.logger.info(f"SheetsManager configurado: output={self.output_file}, backup={self.create_backup}")

    # ========================================================================
    # MÉTODO PRINCIPAL: AGREGAR FILA DE DATOS
    # ========================================================================
    def add_row(self, data: Dict[str, Any]) -> bool:
        """
        Agrega una fila de datos al archivo de salida.
        
        PARÁMETROS:
            data (dict): Diccionario con los datos de la oportunidad
                        Debe contener las claves: Portal, MIA_URL, 
                        MIA_Keywords_Detectadas, MIA_Rubro, MIA_Score_IA,
                        MIA_Resumen_Tecnico
        
        PROCESO:
            1. Valida los datos
            2. Verifica duplicados
            3. (Futuro) Si hay credenciales, escribe en Google Sheets
            4. Escribe en CSV como fallback o método principal
        
        RETORNO:
            bool: True si se agregó exitosamente, False si hubo error o duplicado
        """
        # Validar datos antes de escribir
        if not self._validate_data(data):
            self.logger.error(f"Datos inválidos, no se agregará la fila: {data.get('MIA_URL', 'URL desconocida')}")
            return False
        
        # Verificar duplicados
        url = data.get('MIA_URL', '')
        if url in self.processed_urls:
            self.logger.warning(f"URL duplicada, omitiendo: {url}")
            return False
        
        if self.has_creds:
            # ----------------------------------------------------------------
            # FUTURO: INTEGRACIÓN CON GOOGLE SHEETS
            # ----------------------------------------------------------------
            # TODO: Implementar lógica de GSpread cuando existan credenciales
            # Permitirá sincronización automática con spreadsheet online
            # ----------------------------------------------------------------
            pass
        
        # Escribir en CSV (método actual)
        success = self._write_csv(data)
        
        if success:
            # Agregar URL a conjunto de procesadas
            self.processed_urls.add(url)
        
        return success
        
    # ========================================================================
    # MÉTODO PRIVADO: ESCRIBIR EN ARCHIVO CSV
    # ========================================================================
    def _write_csv(self, data: Dict[str, Any]) -> bool:
        """
        Escribe una fila de datos en el archivo CSV.
        
        PARÁMETROS:
            data (dict): Diccionario con datos de la oportunidad
        
        PROCESO:
            1. Crea backup si es la primera escritura del día
            2. Verifica si el archivo CSV ya existe
            3. Define las columnas del CSV (fieldnames)
            4. Abre archivo en modo append ('a')
            5. Si es nuevo, escribe encabezados primero
            6. Agrega timestamps y metadata
            7. Escribe la fila de datos
        
        CARACTERÍSTICAS:
            - Encoding: UTF-8 (soporta caracteres especiales españoles)
            - Modo: Append (no sobrescribe datos existentes)
            - Newline: '' (evita líneas en blanco en Windows)
            - extrasaction='ignore': Ignora campos extra no definidos
        
        RETORNO:
            bool: True si se escribió exitosamente, False si hubo error
        """
        try:
            # Verificar si el archivo ya existe
            file_exists = os.path.isfile(self.output_file)
            
            # Crear backup si es necesario
            if file_exists and self.create_backup:
                self._create_backup()
            
            # Agregar timestamps y metadata
            enriched_data = self._enrich_data(data)
            
            # Definir columnas del CSV (orden de las columnas)
            fieldnames = [
                "Timestamp_Deteccion",
                "Portal", 
                "MIA_URL", 
                "MIA_Keywords_Detectadas", 
                "MIA_Rubro", 
                "MIA_Score_IA", 
                "MIA_Resumen_Tecnico"
            ]
            
            # Abrir archivo en modo append con encoding UTF-8
            with open(self.output_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                
                # Si el archivo es nuevo, escribir encabezados
                if not file_exists:
                    writer.writeheader()
                    self.logger.info(f"Archivo CSV creado: {self.output_file}")
                
                # Escribir fila de datos
                writer.writerow(enriched_data)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error escribiendo en CSV: {type(e).__name__}: {str(e)}")
            return False
    
    # ========================================================================
    # MÉTODO PRIVADO: VALIDAR DATOS
    # ========================================================================
    def _validate_data(self, data: Dict[str, Any]) -> bool:
        """
        Valida que los datos tengan la estructura correcta.
        
        VALIDACIONES:
            - Campos obligatorios presentes
            - Tipos de datos correctos
            - Valores en rangos válidos
            - URLs válidas
        
        RETORNO:
            bool: True si los datos son válidos, False si no
        """
        required_fields = ['Portal', 'MIA_URL', 'MIA_Rubro', 'MIA_Score_IA']
        
        # Verificar campos obligatorios
        for field in required_fields:
            if field not in data or data[field] is None:
                self.logger.error(f"Campo obligatorio faltante: {field}")
                return False
        
        # Validar URL
        url = data.get('MIA_URL', '')
        if not self._is_valid_url(url):
            self.logger.error(f"URL inválida: {url}")
            return False
        
        # Validar score (0-100)
        score = data.get('MIA_Score_IA')
        if score is not None:
            try:
                score_int = int(score)
                if not (0 <= score_int <= 100):
                    self.logger.error(f"Score fuera de rango (0-100): {score}")
                    return False
            except (ValueError, TypeError):
                self.logger.error(f"Score no es un número válido: {score}")
                return False
        
        return True
    
    # ========================================================================
    # MÉTODO PRIVADO: VALIDAR URL
    # ========================================================================
    def _is_valid_url(self, url: str) -> bool:
        """
        Verifica si una URL es válida.
        
        RETORNO:
            bool: True si es válida, False si no
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    # ========================================================================
    # MÉTODO PRIVADO: ENRIQUECER DATOS CON METADATA
    # ========================================================================
    def _enrich_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Agrega timestamps y metadata a los datos.
        
        RETORNO:
            Dict con datos enriquecidos
        """
        enriched = data.copy()
        
        # Agregar timestamp de detección
        enriched['Timestamp_Deteccion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return enriched
    
    # ========================================================================
    # MÉTODO PRIVADO: CREAR BACKUP
    # ========================================================================
    def _create_backup(self) -> None:
        """
        Crea un backup del archivo CSV actual.
        
        FUNCIONAMIENTO:
            - Solo crea un backup por día
            - Nombre: results_stage1_backup_YYYYMMDD.csv
            - Ubicación: directorio de backups
        """
        if not os.path.exists(self.output_file):
            return
        
        # Nombre del backup con fecha
        today = datetime.now().strftime('%Y%m%d')
        backup_filename = f"{os.path.splitext(os.path.basename(self.output_file))[0]}_backup_{today}.csv"
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        # Solo crear backup si no existe uno para hoy
        if not os.path.exists(backup_path):
            try:
                shutil.copy2(self.output_file, backup_path)
                self.logger.info(f"Backup creado: {backup_path}")
            except Exception as e:
                self.logger.error(f"Error creando backup: {type(e).__name__}: {str(e)}")
    
    # ========================================================================
    # MÉTODO PRIVADO: CARGAR URLs PROCESADAS
    # ========================================================================
    def _load_processed_urls(self) -> None:
        """
        Carga las URLs ya procesadas del CSV existente.
        
        OBJETIVO:
            Evitar procesar duplicados entre ejecuciones
        """
        if not os.path.exists(self.output_file):
            return
        
        try:
            with open(self.output_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    url = row.get('MIA_URL')
                    if url:
                        self.processed_urls.add(url)
            
            self.logger.info(f"Cargadas {len(self.processed_urls)} URLs procesadas previamente")
            
        except Exception as e:
            self.logger.warning(f"No se pudieron cargar URLs procesadas: {type(e).__name__}: {str(e)}")
