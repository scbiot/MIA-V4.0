# MIA V4.0 - Monitor de Inteligencia de Adquisiciones

<div align="center">

![Version](https://img.shields.io/badge/version-4.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![Status](https://img.shields.io/badge/status-Stage%201-yellow.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)

**Sistema inteligente de detección y análisis de oportunidades comerciales en portales de compras públicas**

[Instalación](#-instalación) • [Uso](#-uso-rápido) • [Documentación](#-documentación) • [Roadmap](#-roadmap)

</div>

---

## 📖 Descripción

**MIA V4.0** (Monitor de Inteligencia de Adquisiciones) es un sistema automatizado que:

1. 🔍 **Escanea** portales de compras públicas en busca de licitaciones y oportunidades
2. 🤖 **Analiza** cada oportunidad con Inteligencia Artificial (Google Gemini)
3. 📊 **Clasifica** por rubros (Purificación de Agua / Tratamiento de Efluentes)
4. 💾 **Exporta** resultados a CSV y Google Sheets
5. 📧 **Notifica** oportunidades relevantes por email

### 🎯 Objetivo de Negocio

Detectar automáticamente oportunidades comerciales en los sectores de:
- **Purificación de Agua**: Ingeniería, provisión, servicios y gestión hídrica
- **Tratamiento de Efluentes**: Ingeniería, provisión, servicios y gestión hídrica

---

## ✨ Características Actuales (Stage 1)

- ✅ Scraping de 3 portales principales (comprar.gob.ar, contratar.gob.ar, boletinoficial.gob.ar)
- ✅ Detección con 18 triggers (licitaciones, concursos, proyectos, etc.)
- ✅ Análisis con IA (Google Gemini) en español
- ✅ Clasificación automática por rubros
- ✅ Score de relevancia (0-100)
- ✅ Exportación a CSV
- ✅ Logging detallado de ejecuciones
- ✅ Código completamente documentado en español

---

## 🚀 Instalación

### Requisitos Previos
- Python 3.9 o superior
- Conexión a internet
- API Key de Google Gemini ([obtener aquí](https://makersuite.google.com/app/apikey))

### Instalación Rápida

```bash
# 1. Clonar repositorio
git clone <URL_REPOSITORIO>
cd MIA-V4.0

# 2. Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux

# 5. Editar .env y agregar tu GEMINI_API_KEY
```

📚 **Guía detallada**: Ver [INSTALL.md](INSTALL.md)

---

## 💻 Uso Rápido

### Ejecución Manual

```bash
python main.py
```

El sistema:
1. Se conectará a los portales activos
2. Buscará oportunidades con los triggers configurados
3. Analizará cada una con Gemini AI
4. Guardará resultados en `results_stage1.csv`

### Resultados

Abre `results_stage1.csv` para ver:
- Portal donde se detectó la oportunidad
- URL directa
- Keywords que activaron la detección
- Clasificación por rubro
- Score de relevancia (0-100)
- Resumen técnico en español

---

## 📁 Estructura del Proyecto

```
MIA-V4.0/
│
├── 📄 main.py                      # Punto de entrada principal
├── 📄 requirements.txt             # Dependencias
├── 📄 .env.example                 # Plantilla de configuración
├── 📄 .gitignore                   # Archivos ignorados por Git
│
├── 📂 src/                         # Código fuente
│   ├── 📄 scraper.py               # Motor de scraping
│   ├── 📄 analyzer.py              # Análisis con IA
│   ├── 📄 config.py                # Configuración centralizada
│   └── 📄 sheets_manager.py        # Gestión de salida
│
├── 📂 config/                      # Archivos de configuración
│   └── 📄 prompts.json             # Plantillas de prompts IA
│
├── 📂 docs/                        # Documentación
│   ├── 📄 INSTALL.md               # Guía de instalación
│   ├── 📄 PLAN_IMPLEMENTACION.md   # Roadmap del proyecto
│   └── 📄 DOCUMENTACION_ETAPAS_0_1.md  # Documentación técnica
│
└── 📂 outputs/                     # Resultados (generados)
    ├── 📄 results_stage1.csv       # Resultados en CSV
    └── 📄 historial_ejecuciones.txt  # Log de ejecuciones
```

---

## 📚 Documentación

| Documento | Descripción |
|-----------|-------------|
| [INSTALL.md](INSTALL.md) | Guía completa de instalación paso a paso |
| [PLAN_IMPLEMENTACION.md](PLAN_IMPLEMENTACION.md) | Roadmap y plan de desarrollo |
| [DOCUMENTACION_ETAPAS_0_1.md](DOCUMENTACION_ETAPAS_0_1.md) | Documentación técnica detallada |
| [requirements.txt](requirements.txt) | Dependencias con versiones específicas |

---

## 🗺️ Roadmap

### ✅ Fase 0: Configuración (COMPLETADA)
- [x] Documentación completa del código
- [x] Archivos de configuración (.env, requirements.txt)
- [x] Guías de instalación y uso

### 🔄 Fase 1: Refactorización Base (EN PROGRESO)
- [ ] Manejo robusto de errores
- [ ] Retry logic y rate limiting
- [ ] Sistema de logging mejorado
- [ ] Validación de datos

### 📅 Fase 2: Expansión de Portales (PLANEADA)
- [ ] Activar 34 portales adicionales
- [ ] Implementar Selenium para JavaScript
- [ ] Soporte para autenticación

### 🎯 Fase 3: Búsqueda Inteligente (PLANEADA)
- [ ] Activar 8 rubros con ~300 keywords
- [ ] Lógica de búsqueda combinada
- [ ] Optimización de prompts

### ☁️ Fase 4: Google Sheets (PLANEADA)
- [ ] Integración con Google Sheets API
- [ ] Dashboard automático
- [ ] Notificaciones por email

### ⏰ Fase 5: Automatización (PLANEADA)
- [ ] Scheduler para ejecución periódica
- [ ] Monitoreo y alertas
- [ ] Deployment como servicio

📋 **Plan completo**: Ver [PLAN_IMPLEMENTACION.md](PLAN_IMPLEMENTACION.md)

---

## ⚙️ Configuración

### Variables de Entorno Principales

Edita el archivo `.env`:

```env
# OBLIGATORIO
GEMINI_API_KEY=tu_api_key_aqui

# OPCIONAL (valores por defecto)
GEMINI_MODEL=gemini-flash-latest
LOG_LEVEL=INFO
SCRAPER_TIMEOUT=15
OUTPUT_CSV_FILE=results_stage1.csv
```

### Personalización

- **Portales**: Editar `src/config.py` → `PORTALS`
- **Triggers**: Editar `src/config.py` → `TRIGGERS`
- **Prompts IA**: Editar `config/prompts.json`
- **Columnas CSV**: Editar `src/sheets_manager.py` → `fieldnames`

---

## 🧪 Testing

```bash
# Verificar instalación
python -c "from src.config import GEMINI_API_KEY; print('✅ OK' if GEMINI_API_KEY else '❌ Error')"

# Ejecutar prueba
python main.py
```

---

## 🐛 Solución de Problemas

### Error común: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Error común: "GEMINI_API_KEY not found"
1. Verifica que `.env` existe
2. Verifica que `GEMINI_API_KEY=tu_clave` está configurado
3. Reinicia el programa

### Más ayuda
Ver sección "Solución de Problemas" en [INSTALL.md](INSTALL.md)

---

## 📊 Métricas de Éxito

**Objetivos actuales (Stage 1)**:
- ✅ 3 portales activos
- ✅ 18 triggers configurados
- ✅ Análisis con IA en español
- ✅ Exportación a CSV funcional

**Objetivos futuros**:
- 🎯 37 portales activos (100%)
- 🎯 >50 oportunidades detectadas/mes
- 🎯 >70% de oportunidades relevantes (score >60)
- 🎯 <24 horas desde publicación hasta detección

---

## 🤝 Contribución

Este es un proyecto interno de Water Tech S.A.

Para sugerencias o reportar problemas:
1. Documenta el problema en detalle
2. Incluye logs relevantes
3. Contacta al equipo de desarrollo

---

## 📄 Licencia

**Propietario**: Water Tech S.A.  
**Uso**: Interno exclusivo  
**Confidencialidad**: Todos los derechos reservados

---

## 👥 Equipo

**Desarrollado por**: Water Tech S.A.  
**Versión**: 4.0 - Stage 1  
**Última actualización**: Diciembre 2025

---

## 📞 Soporte

- **Documentación Técnica**: [DOCUMENTACION_ETAPAS_0_1.md](DOCUMENTACION_ETAPAS_0_1.md)
- **Plan de Desarrollo**: [PLAN_IMPLEMENTACION.md](PLAN_IMPLEMENTACION.md)
- **Instalación**: [INSTALL.md](INSTALL.md)

---

<div align="center">

**MIA V4.0** - Detectando oportunidades, impulsando el negocio 🚀

</div>
