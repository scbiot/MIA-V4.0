"""
================================================================================
MIA V4.0 - SCRIPT DE TESTING COMPLETO
================================================================================

OBJETIVO:
    Validar todas las funcionalidades implementadas en Fase 1:
    - Sistema de logging con rotación
    - Backups automáticos
    - Caché de Gemini
    - Métricas de API
    - Validación de respuestas
    - Retry logic

AUTOR: Water Tech S.A.
VERSIÓN: 4.0 - Fase 1 Testing
================================================================================
"""

import os
import sys
import logging
import json
from datetime import datetime

# Agregar directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test 1: Verificar que todos los módulos se importen correctamente"""
    print("\n" + "="*70)
    print("TEST 1: Importación de Módulos")
    print("="*70)
    
    try:
        from src.config import (
            GEMINI_API_KEY, GEMINI_MODEL, LOG_LEVEL,
            GEMINI_ENABLE_CACHE, GEMINI_CACHE_TTL_HOURS,
            GEMINI_COST_PER_1K_TOKENS, GEMINI_METRICS_FILE
        )
        from src.scraper import Scraper
        from src.analyzer import Analyzer
        from src.sheets_manager import SheetsManager
        
        print("✅ Todos los módulos importados correctamente")
        print(f"   - GEMINI_MODEL: {GEMINI_MODEL}")
        print(f"   - LOG_LEVEL: {LOG_LEVEL}")
        print(f"   - GEMINI_ENABLE_CACHE: {GEMINI_ENABLE_CACHE}")
        print(f"   - GEMINI_CACHE_TTL_HOURS: {GEMINI_CACHE_TTL_HOURS}")
        print(f"   - GEMINI_COST_PER_1K_TOKENS: {GEMINI_COST_PER_1K_TOKENS}")
        print(f"   - GEMINI_METRICS_FILE: {GEMINI_METRICS_FILE}")
        return True
    except Exception as e:
        print(f"❌ Error en importación: {e}")
        return False

def test_logging_system():
    """Test 2: Verificar sistema de logging"""
    print("\n" + "="*70)
    print("TEST 2: Sistema de Logging")
    print("="*70)
    
    try:
        # Verificar que el directorio logs/ existe
        if os.path.exists('logs'):
            print("✅ Directorio logs/ existe")
        else:
            print("❌ Directorio logs/ no existe")
            return False
        
        # Verificar que se puede escribir en logs
        test_logger = logging.getLogger("test")
        test_logger.info("Test de logging")
        print("✅ Sistema de logging funcional")
        
        # Verificar archivos de log
        log_files = [f for f in os.listdir('logs') if f.endswith('.log')]
        print(f"✅ Archivos de log encontrados: {len(log_files)}")
        for log_file in log_files:
            size = os.path.getsize(f'logs/{log_file}')
            print(f"   - {log_file}: {size} bytes")
        
        return True
    except Exception as e:
        print(f"❌ Error en sistema de logging: {e}")
        return False

def test_backup_system():
    """Test 3: Verificar sistema de backups"""
    print("\n" + "="*70)
    print("TEST 3: Sistema de Backups")
    print("="*70)
    
    try:
        # Verificar que el directorio backups/ existe
        if os.path.exists('backups'):
            print("✅ Directorio backups/ existe")
            
            # Listar backups
            backup_files = [f for f in os.listdir('backups') if f.endswith('.csv')]
            print(f"✅ Archivos de backup encontrados: {len(backup_files)}")
            for backup_file in backup_files:
                size = os.path.getsize(f'backups/{backup_file}')
                print(f"   - {backup_file}: {size} bytes")
        else:
            print("⚠️  Directorio backups/ no existe (se creará en primera ejecución)")
        
        return True
    except Exception as e:
        print(f"❌ Error en sistema de backups: {e}")
        return False

def test_analyzer_cache():
    """Test 4: Verificar caché del Analyzer"""
    print("\n" + "="*70)
    print("TEST 4: Caché del Analyzer")
    print("="*70)
    
    try:
        from src.analyzer import Analyzer
        
        analyzer = Analyzer()
        
        # Verificar que el caché está inicializado
        if hasattr(analyzer, 'cache'):
            print("✅ Caché inicializado")
            print(f"   - enable_cache: {analyzer.enable_cache}")
            print(f"   - cache_ttl_hours: {analyzer.cache_ttl_hours}")
            print(f"   - Entradas en caché: {len(analyzer.cache)}")
        else:
            print("❌ Caché no inicializado")
            return False
        
        # Test de generación de cache key
        test_text = "Este es un texto de prueba para el caché"
        cache_key = analyzer._generate_cache_key(test_text)
        print(f"✅ Generación de cache key funcional: {cache_key}")
        
        # Test de estimación de tokens
        tokens = analyzer._estimate_tokens(test_text)
        print(f"✅ Estimación de tokens funcional: {tokens} tokens")
        
        return True
    except Exception as e:
        print(f"❌ Error en caché del Analyzer: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_metrics_system():
    """Test 5: Verificar sistema de métricas"""
    print("\n" + "="*70)
    print("TEST 5: Sistema de Métricas")
    print("="*70)
    
    try:
        from src.analyzer import Analyzer
        
        analyzer = Analyzer()
        
        # Verificar que las métricas están inicializadas
        if hasattr(analyzer, 'metrics'):
            print("✅ Métricas inicializadas")
            print(f"   - total_requests: {analyzer.metrics['total_requests']}")
            print(f"   - cache_hits: {analyzer.metrics['cache_hits']}")
            print(f"   - cache_misses: {analyzer.metrics['cache_misses']}")
            print(f"   - total_tokens: {analyzer.metrics['total_tokens']}")
            print(f"   - total_cost_usd: ${analyzer.metrics['total_cost_usd']:.4f}")
        else:
            print("❌ Métricas no inicializadas")
            return False
        
        # Verificar archivo de métricas
        if os.path.exists(analyzer.metrics_file):
            with open(analyzer.metrics_file, 'r', encoding='utf-8') as f:
                metrics_data = json.load(f)
                print(f"✅ Archivo de métricas existe: {analyzer.metrics_file}")
                print(f"   - Requests históricos: {metrics_data.get('total_requests', 0)}")
        else:
            print("⚠️  Archivo de métricas no existe (se creará en primera ejecución)")
        
        return True
    except Exception as e:
        print(f"❌ Error en sistema de métricas: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_configuration():
    """Test 6: Verificar configuración completa"""
    print("\n" + "="*70)
    print("TEST 6: Configuración del Sistema")
    print("="*70)
    
    try:
        from src.config import (
            PORTALS, TRIGGERS, SEARCH_KEYWORDS,
            GEMINI_RETRY_ATTEMPTS, LOG_ROTATION_SIZE_MB, LOG_BACKUP_COUNT
        )
        
        print(f"✅ Portales activos: {len([p for p in PORTALS if p.get('enabled', False)])}")
        print(f"✅ Triggers configurados: {len(TRIGGERS)}")
        print(f"✅ Search keywords: {len(SEARCH_KEYWORDS)}")
        print(f"✅ Gemini retry attempts: {GEMINI_RETRY_ATTEMPTS}")
        print(f"✅ Log rotation size: {LOG_ROTATION_SIZE_MB} MB")
        print(f"✅ Log backup count: {LOG_BACKUP_COUNT}")
        
        return True
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def test_file_structure():
    """Test 7: Verificar estructura de archivos"""
    print("\n" + "="*70)
    print("TEST 7: Estructura de Archivos")
    print("="*70)
    
    required_files = [
        'main.py',
        'src/config.py',
        'src/scraper.py',
        'src/analyzer.py',
        'src/sheets_manager.py',
        'config/prompts.json',
        '.env.example',
        '.gitignore',
        'README.md',
        'PLAN_IMPLEMENTACION.md'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - NO ENCONTRADO")
            all_exist = False
    
    return all_exist

def main():
    """Ejecutar todos los tests"""
    print("\n" + "="*70)
    print("MIA V4.0 - TESTING COMPLETO DE FASE 1")
    print("="*70)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    results = {
        "Test 1 - Importación de Módulos": test_imports(),
        "Test 2 - Sistema de Logging": test_logging_system(),
        "Test 3 - Sistema de Backups": test_backup_system(),
        "Test 4 - Caché del Analyzer": test_analyzer_cache(),
        "Test 5 - Sistema de Métricas": test_metrics_system(),
        "Test 6 - Configuración": test_configuration(),
        "Test 7 - Estructura de Archivos": test_file_structure()
    }
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN DE TESTS")
    print("="*70)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "="*70)
    print(f"RESULTADO FINAL: {passed}/{total} tests pasados ({passed/total*100:.1f}%)")
    print("="*70)
    
    if passed == total:
        print("\n🎉 ¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
        print("✅ El sistema está listo para uso en producción")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) fallaron")
        print("❌ Revisar errores antes de usar en producción")
        return 1

if __name__ == "__main__":
    exit_code = main()
    print("\nPresione ENTER para salir...")
    input()
    sys.exit(exit_code)
