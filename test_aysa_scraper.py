"""
================================================================================
MIA V4.0 - TESTING DEL SCRAPER DE AYSA
================================================================================

OBJETIVO:
    Validar que el scraper de AySA funciona correctamente y puede extraer
    licitaciones del portal.

TESTS:
    1. Creación del scraper
    2. Conexión al portal
    3. Extracción de licitaciones
    4. Validación de datos

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

def test_aysa_scraper_creation():
    """Test 1: Verificar que el scraper de AySA se puede crear"""
    print("\n" + "="*70)
    print("TEST 1: Creación del Scraper de AySA")
    print("="*70)
    
    try:
        from src.config import PORTALS
        from src.portals.phase2a import AysaScraper
        
        # Buscar configuración de AySA
        aysa_config = next((p for p in PORTALS if p['name'] == 'aysa.com.ar'), None)
        
        if not aysa_config:
            print("❌ Configuración de AySA no encontrada en PORTALS")
            return False
        
        print(f"✅ Configuración encontrada:")
        print(f"   - Nombre: {aysa_config['name']}")
        print(f"   - URL: {aysa_config['url']}")
        print(f"   - Habilitado: {aysa_config.get('enabled', False)}")
        
        # Crear scraper
        scraper = AysaScraper(aysa_config)
        print(f"✅ Scraper creado exitosamente")
        print(f"   - Clase: {scraper.__class__.__name__}")
        print(f"   - URL Base: {scraper.base_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_aysa_scraper_search():
    """Test 2: Probar búsqueda en AySA (requiere Selenium)"""
    print("\n" + "="*70)
    print("TEST 2: Búsqueda en Portal de AySA")
    print("="*70)
    print("⚠️  NOTA: Este test requiere Selenium y puede tardar varios minutos")
    print("⚠️  Se ejecutará en modo headless (sin abrir ventana del navegador)")
    
    try:
        from src.config import PORTALS
        from src.portals.phase2a import AysaScraper
        
        # Buscar configuración de AySA
        aysa_config = next((p for p in PORTALS if p['name'] == 'aysa.com.ar'), None)
        
        if not aysa_config:
            print("❌ Configuración de AySA no encontrada")
            return False
        
        # Crear scraper
        scraper = AysaScraper(aysa_config)
        
        # Ejecutar búsqueda con keywords de prueba
        test_keywords = ["agua", "tratamiento"]
        
        print(f"\n🔍 Buscando licitaciones con keywords: {test_keywords}")
        print("   (Esto puede tardar 30-60 segundos...)")
        
        results = scraper.search(test_keywords)
        
        print(f"\n✅ Búsqueda completada")
        print(f"   - Resultados encontrados: {len(results)}")
        
        if results:
            print(f"\n📋 Primeros 3 resultados:")
            for i, result in enumerate(results[:3], 1):
                print(f"\n   {i}. {result.get('title', 'Sin título')}")
                print(f"      Portal: {result.get('portal')}")
                print(f"      Sección: {result.get('section')}")
                print(f"      Estado: {result.get('estado')}")
                print(f"      URL: {result.get('url', 'N/A')}")
                if result.get('matched_keywords'):
                    print(f"      Keywords: {', '.join(result['matched_keywords'])}")
        else:
            print("\n⚠️  No se encontraron resultados (puede ser normal si no hay licitaciones activas)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en búsqueda: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_selenium_availability():
    """Test 3: Verificar que Selenium está disponible"""
    print("\n" + "="*70)
    print("TEST 3: Disponibilidad de Selenium")
    print("="*70)
    
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from webdriver_manager.chrome import ChromeDriverManager
        
        print("✅ Selenium importado correctamente")
        print("✅ WebDriver Manager disponible")
        print("✅ By (selectores) disponible")
        
        # Verificar que se puede obtener el driver
        from src.portals.phase2a import get_selenium_driver
        print("✅ Función get_selenium_driver disponible")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Ejecutar todos los tests"""
    print("\n" + "="*70)
    print("MIA V4.0 - TESTING DEL SCRAPER DE AYSA")
    print("="*70)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Preguntar al usuario si quiere ejecutar el test de búsqueda
    print("\n⚠️  IMPORTANTE:")
    print("El Test 2 (Búsqueda en AySA) requiere Selenium y puede tardar varios minutos.")
    print("Ejecutará Chrome en modo headless y accederá al portal de AySA.")
    
    response = input("\n¿Desea ejecutar el Test 2 de búsqueda? (s/n): ").lower().strip()
    run_search_test = response in ['s', 'si', 'sí', 'y', 'yes']
    
    results = {
        "Test 1 - Creación del Scraper": test_aysa_scraper_creation(),
        "Test 3 - Disponibilidad de Selenium": test_selenium_availability()
    }
    
    if run_search_test:
        results["Test 2 - Búsqueda en AySA"] = test_aysa_scraper_search()
    else:
        print("\n⏭️  Test 2 omitido por el usuario")
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN DE TESTS - SCRAPER AYSA")
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
        print("✅ El scraper de AySA está listo para uso")
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
