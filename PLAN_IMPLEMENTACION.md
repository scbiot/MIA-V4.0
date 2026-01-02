# Plan de Implementación MIA V4.0

## 📋 Estado Actual del Proyecto

### ✅ Completado
- **Documentación Etapas 0 y 1**: Todos los archivos Python y JSON documentados en español
- **Estructura Base**: Sistema funcional con scraping, análisis IA y salida CSV
- **Configuración**: Portales Group 1 activos, 18 triggers, prompts externalizados
- **Validación**: Todos los archivos validados sin errores de sintaxis
- **Fase 0**: ✅ COMPLETADA (100%) - Archivos de configuración creados
- **Fase 1**: ✅ COMPLETADA (100%) - 32 de 32 tareas completadas
- **Análisis de Portales**: ✅ COMPLETADO - Informe de 34 portales generado
- **Repositorio GitHub**: ✅ CONFIGURADO - Sincronizado con github.com/scbiot/MIA-V4.0
- **Testing**: ✅ COMPLETADO - 7/7 tests pasados (100%)

### 🎯 Objetivo General
Evolucionar MIA V4.0 de un sistema básico (Stage 1) a una plataforma robusta, escalable y mantenible que detecte y analice oportunidades comerciales en portales de compras públicas.

---

## 🗺️ Roadmap de Implementación

### **FASE 0: Configuración y Preparación** ✅ COMPLETADA
**Objetivo**: Establecer fundamentos para desarrollo escalable
**Duración**: 1 día (2025-12-10)
**Estado**: ✅ 100% Completada

#### Tareas:
- [x] ✅ Documentar código existente
- [x] ✅ Crear archivo de configuración de entorno (.env.example)
- [x] ✅ Documentar requisitos del sistema (requirements.txt detallado)
- [x] ✅ Crear guía de instalación (INSTALL.md)
- [x] ✅ Establecer estructura de directorios estándar
- [x] ✅ Crear README.md principal
- [x] ✅ Crear .gitignore
- [x] ✅ Definir métricas de éxito

**Entregables**:
- ✅ `.env.example` - Plantilla de variables de entorno (150 líneas)
- ✅ `INSTALL.md` - Guía de instalación paso a paso (380 líneas)
- ✅ `requirements.txt` - Dependencias con versiones específicas (140 líneas)
- ✅ `README.md` - Documentación principal (320 líneas)
- ✅ `.gitignore` - Control de versiones (250 líneas)
- ✅ `PLAN_IMPLEMENTACION.md` - Este documento (367 líneas)
- ✅ `INFORME_ANALISIS_PORTALES.md` - Análisis de 34 portales (800+ líneas)

---

### **FASE 1: Refactorización y Mejoras Base** ✅ COMPLETADA (100%)
**Objetivo**: Mejorar robustez y mantenibilidad del código actual
**Duración**: 5 días
**Estado**: ✅ 32 de 32 tareas completadas
**Última Actualización**: 2026-01-02
**Fecha de Completitud**: 2026-01-02

#### 1.1 Mejoras en Scraper ✅ 10/10 completadas
- [x] ✅ Implementar manejo robusto de errores HTTP (9 códigos específicos)
- [x] ✅ Agregar retry logic con backoff exponencial
- [x] ✅ Implementar rate limiting para evitar bloqueos
- [x] ✅ Agregar user-agent configurable
- [x] ✅ Implementar timeout configurables
- [x] ✅ Agregar logging detallado de conexiones
- [x] ✅ Headers HTTP realistas
- [x] ✅ Jitter aleatorio en retry
- [x] ✅ Implementar rotación de múltiples user-agents
- [x] ✅ Manejo de cookies/sessions

#### 1.2 Mejoras en Analyzer ✅ 5/5 completadas
- [x] ✅ Agregar validación de respuestas JSON
- [x] ✅ Implementar fallback para errores de API (retry con backoff)
- [x] ✅ Optimizar uso de tokens (truncamiento inteligente a 10k caracteres)
- [x] ✅ Implementar caché de respuestas de Gemini con TTL
- [x] ✅ Agregar métricas de costo de API (tokens, costo, cache hit rate)

#### 1.3 Mejoras en SheetsManager ✅ 5/5 completadas
- [x] ✅ Implementar validación de datos antes de escribir
- [x] ✅ Agregar manejo de duplicados
- [x] ✅ Implementar backup automático de CSV
- [x] ✅ Agregar timestamps a cada registro
- [x] ✅ Preparar estructura para Google Sheets API

#### 1.4 Sistema de Logging Mejorado ✅ 4/4 completadas
- [x] ✅ Implementar niveles de log configurables (DEBUG/INFO/WARNING/ERROR desde .env)
- [x] ✅ Agregar rotación de archivos de log (RotatingFileHandler)
- [x] ✅ Crear logs organizados en directorio logs/
- [x] ✅ Implementar formato consistente de logs con timestamps

**Entregables**:
- ✅ `src/scraper.py` - Refactorizado con retry logic y manejo de errores (+200 líneas)
- ✅ `src/sheets_manager.py` - Reescrito con validación y backups (+100 líneas)
- ✅ `src/analyzer.py` - Mejorado con caché y métricas (+250 líneas)
- ✅ `main.py` - Sistema de logging mejorado (+80 líneas)
- ✅ `src/config.py` - Nuevas configuraciones (+20 líneas)
- ✅ `test_phase1.py` - Script de testing completo (nuevo)
- ✅ `RESUMEN_FASE1_SESION1.md` - Documentación de cambios
- ✅ `RESUMEN_FASE1_ACTUALIZADO.md` - Resumen completo
- ✅ Sistema de logging robusto con rotación
- ✅ Caché de Gemini con TTL configurable
- ✅ Métricas de API persistentes en JSON

---

### **FASE 2: Expansión de Portales** ⏱️ 5-7 días
**Objetivo**: Activar más portales y mejorar estrategias de scraping
**Estado**: ⏳ Análisis completado, implementación pendiente

#### 2.1 Análisis de Portales ✅ COMPLETADO
- [x] ✅ Analizar estructura de cada portal inactivo (34 portales)
- [x] ✅ Identificar métodos de autenticación requeridos
- [x] ✅ Documentar estrategias de scraping por portal
- [x] ✅ Priorizar portales por valor de negocio (4 fases: 2A-2D)
- [x] ✅ Generar informe detallado (INFORME_ANALISIS_PORTALES.md)

**Portales Críticos Identificados (Fase 2A)**:
- 🔴 **aysa.com.ar** - Empresa de agua (100% relevante)
- 🔴 **proveedores.ypf.com** - YPF (grandes proyectos)
- 🔴 **opc.gba.gob.ar** - Provincia de Buenos Aires
- 🔴 **buenosairescompras.gob.ar** - Ciudad de Buenos Aires

#### 2.2 Implementación por Grupos ⏳ PENDIENTE
- [ ] **Fase 2A**: 4 Portales Críticos (aysa, ypf, opc.gba, buenosairescompras)
- [ ] **Fase 2B**: 6 Portales Alta Prioridad (universidades, córdoba, afip, etc.)
- [ ] **Fase 2C**: 10 Portales Provinciales/Municipales
- [ ] **Fase 2D**: 14 Portales Empresas Privadas (opcional)

#### 2.3 Técnicas Avanzadas de Scraping
- [ ] Implementar Selenium para portales con JavaScript
- [ ] Agregar soporte para autenticación (OAuth, cookies)
- [ ] Implementar scraping de PDFs
- [ ] Agregar extracción de tablas estructuradas
- [ ] Implementar detección de cambios en portales

**Entregables**:
- 34 portales adicionales activos
- Documentación de estrategias por portal
- Tests de scraping por portal

---

### **FASE 3: Búsqueda Inteligente por Rubros** ⏱️ 4-6 días
**Objetivo**: Implementar lógica de búsqueda combinada (TRIGGERS AND KEYWORDS)

#### 3.1 Activación de Rubros
- [ ] Activar keywords de Rubro 1: Purificación - Ingeniería
- [ ] Activar keywords de Rubro 2: Purificación - Provisión
- [ ] Activar keywords de Rubro 3: Purificación - Servicios
- [ ] Activar keywords de Rubro 4: Purificación - Gestión Hídrica
- [ ] Activar keywords de Rubro 5: Efluentes - Ingeniería
- [ ] Activar keywords de Rubro 6: Efluentes - Provisión
- [ ] Activar keywords de Rubro 7: Efluentes - Servicios
- [ ] Activar keywords de Rubro 8: Efluentes - Gestión Hídrica

#### 3.2 Lógica de Búsqueda
- [ ] Implementar búsqueda combinada (TRIGGER AND KEYWORD)
- [ ] Agregar scoring por relevancia de keywords
- [ ] Implementar filtros configurables
- [ ] Agregar detección de contexto (NLP básico)

#### 3.3 Optimización de Prompts
- [ ] Crear prompts específicos por rubro
- [ ] Implementar few-shot learning en prompts
- [ ] Optimizar para reducir tokens
- [ ] A/B testing de diferentes prompts

**Entregables**:
- 8 rubros activos con ~300 keywords técnicas
- Lógica de búsqueda combinada implementada
- Prompts optimizados por rubro

---

### **FASE 4: Integración con Google Sheets** ⏱️ 3-4 días
**Objetivo**: Sincronización automática con Google Sheets

#### 4.1 Configuración de API
- [ ] Crear proyecto en Google Cloud Console
- [ ] Habilitar Google Sheets API
- [ ] Crear credenciales de servicio
- [ ] Configurar permisos de spreadsheet

#### 4.2 Implementación
- [ ] Implementar autenticación con gspread
- [ ] Crear funciones de escritura a Sheets
- [ ] Implementar sincronización bidireccional
- [ ] Agregar manejo de cuotas de API
- [ ] Implementar batch updates para eficiencia

#### 4.3 Features Avanzadas
- [ ] Crear dashboard automático en Sheets
- [ ] Implementar fórmulas y formato condicional
- [ ] Agregar gráficos automáticos
- [ ] Implementar notificaciones por email

**Entregables**:
- Integración completa con Google Sheets
- Dashboard automático
- Sistema de notificaciones

---

### **FASE 5: Automatización y Scheduling** ⏱️ 2-3 días
**Objetivo**: Ejecución automática periódica

#### 5.1 Scheduler
- [ ] Implementar scheduler con APScheduler
- [ ] Configurar ejecuciones periódicas (diaria, semanal)
- [ ] Agregar configuración de horarios
- [ ] Implementar manejo de concurrencia

#### 5.2 Monitoreo
- [ ] Implementar health checks
- [ ] Agregar alertas por errores
- [ ] Crear dashboard de métricas
- [ ] Implementar logging de métricas de negocio

#### 5.3 Deployment
- [ ] Crear script de deployment
- [ ] Configurar como servicio de Windows
- [ ] Implementar auto-restart en caso de fallo
- [ ] Documentar proceso de deployment

**Entregables**:
- Sistema automatizado con scheduler
- Monitoreo y alertas
- Proceso de deployment documentado

---

### **FASE 6: Testing y Calidad** ⏱️ 3-5 días
**Objetivo**: Asegurar calidad y confiabilidad del sistema

#### 6.1 Tests Unitarios
- [ ] Tests para Scraper (mocking de requests)
- [ ] Tests para Analyzer (mocking de Gemini API)
- [ ] Tests para SheetsManager
- [ ] Tests para config y utils

#### 6.2 Tests de Integración
- [ ] Tests end-to-end del flujo completo
- [ ] Tests de integración con APIs externas
- [ ] Tests de manejo de errores

#### 6.3 Tests de Performance
- [ ] Benchmarking de scraping
- [ ] Optimización de uso de API
- [ ] Tests de carga

#### 6.4 Calidad de Código
- [ ] Configurar linters (pylint, flake8)
- [ ] Implementar type hints
- [ ] Configurar pre-commit hooks
- [ ] Code review checklist

**Entregables**:
- Suite de tests completa (>80% coverage)
- CI/CD pipeline básico
- Documentación de testing

---

### **FASE 7: Features Avanzadas** ⏱️ 5-7 días
**Objetivo**: Agregar funcionalidades de valor agregado

#### 7.1 Machine Learning
- [ ] Implementar clasificación automática de rubros
- [ ] Agregar predicción de probabilidad de éxito
- [ ] Implementar detección de anomalías
- [ ] Crear modelo de scoring personalizado

#### 7.2 NLP Avanzado
- [ ] Extracción de entidades (montos, fechas, empresas)
- [ ] Análisis de sentimiento
- [ ] Resumen automático mejorado
- [ ] Detección de requisitos técnicos

#### 7.3 Visualización
- [ ] Dashboard web interactivo (Streamlit/Dash)
- [ ] Gráficos de tendencias
- [ ] Mapas de oportunidades por región
- [ ] Análisis de competencia

#### 7.4 Integraciones
- [ ] Integración con CRM
- [ ] Integración con sistema de email
- [ ] Webhooks para notificaciones
- [ ] API REST para consultas

**Entregables**:
- Features de ML implementadas
- Dashboard web interactivo
- Integraciones con sistemas externos

---

## 📊 Priorización por Necesidades de Negocio

### 🔴 **ALTA PRIORIDAD** (Implementar primero)
1. **Fase 0**: Configuración y Preparación
2. **Fase 1**: Refactorización y Mejoras Base
3. **Fase 2**: Expansión de Portales (Groups 2-4)
4. **Fase 4**: Integración con Google Sheets

**Justificación**: Estas fases mejoran la robustez del sistema actual y expanden la cobertura de portales, generando valor inmediato.

### 🟡 **MEDIA PRIORIDAD** (Implementar después)
5. **Fase 3**: Búsqueda Inteligente por Rubros
6. **Fase 5**: Automatización y Scheduling
7. **Fase 2**: Expansión de Portales (Groups 5-8)

**Justificación**: Mejoran la precisión y automatización, pero el sistema puede funcionar sin ellas inicialmente.

### 🟢 **BAJA PRIORIDAD** (Implementar al final)
8. **Fase 6**: Testing y Calidad (puede ir en paralelo)
9. **Fase 7**: Features Avanzadas

**Justificación**: Son mejoras de calidad y features avanzadas que agregan valor pero no son críticas para operación básica.

---

## 🎯 Métricas de Éxito

### Métricas Técnicas
- **Uptime**: >95% de disponibilidad
- **Tasa de Error**: <5% de fallos en scraping
- **Cobertura de Portales**: 37 portales activos (100%)
- **Precisión de Clasificación**: >85% de oportunidades bien clasificadas
- **Tiempo de Ejecución**: <30 minutos por ciclo completo

### Métricas de Negocio
- **Oportunidades Detectadas**: >50 oportunidades/mes
- **Oportunidades Relevantes**: >70% con score >60
- **Tiempo de Detección**: <24 horas desde publicación
- **ROI**: Costo de operación < 10% del valor de oportunidades ganadas

---

## 📅 Timeline Estimado

| Fase | Duración | Inicio | Fin |
|------|----------|--------|-----|
| Fase 0 | 2 días | Semana 1 | Semana 1 |
| Fase 1 | 5 días | Semana 1 | Semana 2 |
| Fase 2 (G2-4) | 7 días | Semana 2 | Semana 3 |
| Fase 4 | 4 días | Semana 3 | Semana 4 |
| Fase 3 | 6 días | Semana 4 | Semana 5 |
| Fase 5 | 3 días | Semana 5 | Semana 5 |
| Fase 2 (G5-8) | 7 días | Semana 6 | Semana 7 |
| Fase 6 | 5 días | Paralelo | Paralelo |
| Fase 7 | 7 días | Semana 8 | Semana 9 |

**Total**: ~9 semanas (2 meses)

---

## 🚀 Progreso y Próximos Pasos

### ✅ Completado (2026-01-02)
1. ✅ Plan de implementación creado y aprobado
2. ✅ Fase 0 completada (100%) - Archivos de configuración
3. ✅ Análisis de 34 portales completado
4. ✅ Fase 1 COMPLETADA (100%) - Todas las mejoras implementadas
5. ✅ Documentación completa generada y actualizada
6. ✅ Testing completo - 7/7 tests pasados
7. ✅ GitHub configurado y sincronizado

### 🔄 En Progreso
6. 🔄 Fase 1 - Refactorización (84% completado)
   - ✅ Scraper: 10/10 tareas (COMPLETADO)
   - ✅ SheetsManager: 5/5 tareas (COMPLETADO)
   - 🔄 Analyzer: 3/5 tareas
   - ✅ Logging: 4/4 tareas (COMPLETADO)
   - ✅ Control de Versiones: GitHub configurado

### ⏳ Próxima Sesión
8. ⏳ Comenzar Fase 2A - Implementar 4 portales críticos:
   - aysa.com.ar (Empresa de agua - 100% relevante)
   - proveedores.ypf.com (YPF - grandes proyectos)
   - opc.gba.gob.ar (Provincia de Buenos Aires)
   - buenosairescompras.gob.ar (Ciudad de Buenos Aires)

---

## 📝 Notas y Consideraciones

### Riesgos Identificados
- **Bloqueo de IPs**: Portales pueden bloquear scraping agresivo
- **Cambios en Portales**: Estructura de sitios puede cambiar
- **Costos de API**: Gemini API tiene costos por uso
- **Mantenimiento**: Sistema requiere monitoreo continuo

### Mitigaciones
- Implementar rate limiting y user-agent rotation
- Crear sistema de detección de cambios
- Optimizar uso de tokens y considerar caché
- Automatizar monitoreo y alertas

---

## ✅ Estado del Plan

**Fecha de Creación**: 2025-12-10  
**Última Actualización**: 2026-01-02 09:45  
**Versión**: 1.2  
**Estado**: ✅ APROBADO Y EN EJECUCIÓN

### Progreso General
- **Fase 0**: ✅ 100% Completada
- **Fase 1**: ✅ 100% Completada (32/32 tareas) - 🎉 FINALIZADA
- **Fase 2**: 🔄 Análisis completado, implementación pendiente
- **Fases 3-7**: ⏳ Pendientes
- **GitHub**: ✅ Repositorio configurado y sincronizado
- **Testing**: ✅ 7/7 tests pasados (100%)

### Archivos Generados
- ✅ PLAN_IMPLEMENTACION.md (este archivo)
- ✅ INFORME_ANALISIS_PORTALES.md
- ✅ RESUMEN_FASE1_SESION1.md
- ✅ DOCUMENTACION_ETAPAS_0_1.md
- ✅ INSTALL.md
- ✅ README.md
- ✅ .env.example
- ✅ requirements.txt
- ✅ .gitignore
- ✅ task.md (artifact)

---

**Próximo Paso**: Una vez aprobado este plan, comenzaremos con **Fase 0** creando los archivos de configuración necesarios.
