"""
================================================================================
MIA V4.0 - TESTING DE SCRAPERS FASE 2A
================================================================================

OBJETIVO:
    Validar que los scrapers de Fase 2A están correctamente configurados
    y pueden ser inicializados sin errores.

TESTS:
    1. Importación de módulos
    2. Creación de scrapers
    3. Configuración de Selenium
    4. Verificación de portales en config

AUTOR: Water Tech S.A.
VERSIÓN: 4.0 - Fase 2A Testing
FECHA: 2026-01-02
================================================================================
"""

import os
import sys
from datetime import datetime

# Agregar directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test 1: Verificar que todos los módulos se importen correctamente"""
    print("\n" + "="*70)
    print("TEST 1: Importación de Módulos Fase 2A")
    print("="*70)
    
    try:
        # Importar módulo de scrapers Fase 2A
        from src.portals.phase2a import (
            AysaScraper,
            OpcGbaScraper,
            BuenosAiresComprasScraper,
            YpfScraper,
            create_phase2a_scraper,
            get_selenium_driver,
            SeleniumHelper
        )
        
        print("✅ Módulo phase2a.py importado correctamente")
        print("   - AysaScraper")
        print("   - OpcGbaScraper")
        print("   - BuenosAiresComprasScraper")
        print("   - YpfScraper")
        print("   - create_phase2a_scraper")
        print("   - get_selenium_driver")
        print("   - SeleniumHelper")
        
        # Importar Selenium
        import selenium
        from selenium import webdriver
        from webdriver_manager.chrome import ChromeDriverManager
        
        print("✅ Selenium importado correctamente")
        print(f"   - Versión: {selenium.__version__}")
        
        return True
    except Exception as e:
        print(f"❌ Error en importación: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_portals():
    """Test 2: Verificar que los portales Fase 2A están en config"""
    print("\n" + "="*70)
    print("TEST 2: Configuración de Portales Fase 2A")
    print("="*70)
    
    try:
        from src.config import PORTALS
        
        # Filtrar portales de Fase 2A
        phase2a_portals = [p for p in PORTALS if p.get('phase') == '2A']
        
        print(f"✅ Portales Fase 2A configurados: {len(phase2a_portals)}")
        
        for portal in phase2a_portals:
            enabled_status = "✅ ACTIVO" if portal.get('enabled') else "⏸️  INACTIVO"
            print(f"\n   {enabled_status} - {portal['name']}")
            print(f"      URL: {portal['url']}")
            print(f"      Tipo: {portal['type']}")
            print(f"      Método: {portal['search_method']}")
            print(f"      Prioridad: {portal.get('priority', 'N/A')}")
            if portal.get('requires_auth'):
                print(f"      ⚠️  Requiere autenticación")
        
        # Verificar que hay exactamente 4 portales
        if len(phase2a_portals) == 4:
            print(f"\n✅ Número correcto de portales Fase 2A: 4")
            return True
        else:
            print(f"\n⚠️  Se esperaban 4 portales, encontrados: {len(phase2a_portals)}")
            return False
            
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_scraper_creation():
    """Test 3: Verificar que los scrapers se pueden crear"""
    print("\n" + "="*70)
    print("TEST 3: Creación de Scrapers")
    print("="*70)
    
    try:
        from src.config import PORTALS
        from src.portals.phase2a import create_phase2a_scraper
        
        # Filtrar portales de Fase 2A habilitados
        phase2a_portals = [p for p in PORTALS if p.get('phase') == '2A' and p.get('enabled')]
        
        scrapers_created = []
        
        for portal_config in phase2a_portals:
            try:
                scraper = create_phase2a_scraper(portal_config)
                scrapers_created.append(portal_config['name'])
                print(f"✅ Scraper creado: {portal_config['name']}")
                print(f"   - Clase: {scraper.__class__.__name__}")
                print(f"   - URL Base: {scraper.base_url}")
            except Exception as e:
                print(f"❌ Error creando scraper para {portal_config['name']}: {e}")
        
        print(f"\n✅ Scrapers creados exitosamente: {len(scrapers_created)}/{len(phase2a_portals)}")
        
        return len(scrapers_created) == len(phase2a_portals)
        
    except Exception as e:
        print(f"❌ Error en creación de scrapers: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_selenium_config():
    """Test 4: Verificar configuración de Selenium (sin inicializar driver)"""
    print("\n" + "="*70)
    print("TEST 4: Configuración de Selenium")
    print("="*70)
    
    try:
        from src.portals.phase2a import get_selenium_driver, SeleniumHelper
        from selenium.webdriver.chrome.options import Options
        
        print("✅ Función get_selenium_driver disponible")
        print("✅ Clase SeleniumHelper disponible")
        
        # Verificar que Options se puede crear
        options = Options()
        print("✅ Chrome Options se puede crear")
        
        # Verificar métodos de SeleniumHelper
        methods = ['wait_for_element', 'safe_click', 'extract_text_safe']
        for method in methods:
            if hasattr(SeleniumHelper, method):
                print(f"✅ Método SeleniumHelper.{method} disponible")
            else:
                print(f"❌ Método SeleniumHelper.{method} NO disponible")
                return False
        
        print("\n⚠️  NOTA: No se inicializa el driver para evitar abrir Chrome")
        print("   El driver se inicializará cuando se ejecuten los scrapers")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración de Selenium: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dependencies():
    """Test 5: Verificar que todas las dependencias están instaladas"""
    print("\n" + "="*70)
    print("TEST 5: Dependencias Instaladas")
    print("="*70)
    
    dependencies = {
        'selenium': 'Selenium WebDriver',
        'webdriver_manager': 'WebDriver Manager',
        'PyPDF2': 'PyPDF2 (extracción de PDFs)',
        'requests': 'Requests (HTTP)',
        'bs4': 'BeautifulSoup4 (HTML parsing)'
    }
    
    all_installed = True
    
    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {description}")
        except ImportError:
            print(f"❌ {description} - NO INSTALADO")
            all_installed = False
    
    return all_installed

def main():
    """Ejecutar todos los tests"""
    print("\n" + "="*70)
    print("MIA V4.0 - TESTING DE FASE 2A")
    print("="*70)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    results = {
        "Test 1 - Importación de Módulos": test_imports(),
        "Test 2 - Configuración de Portales": test_config_portals(),
        "Test 3 - Creación de Scrapers": test_scraper_creation(),
        "Test 4 - Configuración de Selenium": test_selenium_config(),
        "Test 5 - Dependencias": test_dependencies()
    }
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN DE TESTS - FASE 2A")
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
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("✅ Fase 2A está lista para implementación de scrapers")
        print("\n📋 PRÓXIMOS PASOS:")
        print("   1. Investigar estructura de cada portal")
        print("   2. Implementar lógica de scraping específica")
        print("   3. Testing con datos reales")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) fallaron")
        print("❌ Revisar errores antes de continuar")
        return 1

if __name__ == "__main__":
    exit_code = main()
    print("\nPresione ENTER para salir...")
    input()
    sys.exit(exit_code)
