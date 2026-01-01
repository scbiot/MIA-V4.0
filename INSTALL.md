# Guía de Instalación - MIA V4.0

## 📋 Requisitos del Sistema

### Sistema Operativo
- **Windows 10/11** (64-bit)
- **macOS** 10.15 o superior
- **Linux** (Ubuntu 20.04+, Debian 10+, o similar)

### Software Requerido
- **Python 3.9+** (recomendado: Python 3.11)
- **pip** (gestor de paquetes de Python)
- **Git** (para control de versiones)

### Recursos Mínimos
- **RAM**: 4 GB mínimo, 8 GB recomendado
- **Disco**: 500 MB libres
- **Internet**: Conexión estable (para scraping y API calls)

---

## 🚀 Instalación Paso a Paso

### 1. Clonar o Descargar el Proyecto

Si tienes Git instalado:
```bash
git clone <URL_DEL_REPOSITORIO>
cd MIA-V4.0
```

O descarga el proyecto manualmente y extrae en una carpeta.

---

### 2. Crear Entorno Virtual (Recomendado)

#### En Windows:
```powershell
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
.venv\Scripts\activate
```

#### En macOS/Linux:
```bash
# Crear entorno virtual
python3 -m venv .venv

# Activar entorno virtual
source .venv/bin/activate
```

**Nota**: Verás `(.venv)` al inicio de tu línea de comandos cuando el entorno esté activo.

---

### 3. Instalar Dependencias

Con el entorno virtual activado:

```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt
```

**Verificar instalación**:
```bash
pip list
```

Deberías ver todas las librerías listadas en `requirements.txt`.

---

### 4. Configurar Variables de Entorno

#### 4.1 Copiar plantilla de configuración:
```bash
# En Windows (PowerShell)
Copy-Item .env.example .env

# En macOS/Linux
cp .env.example .env
```

#### 4.2 Editar archivo `.env`:

Abre el archivo `.env` con tu editor favorito y completa:

**OBLIGATORIO**:
```env
GEMINI_API_KEY=tu_api_key_aqui
```

**Cómo obtener tu API Key de Gemini**:
1. Visita: https://makersuite.google.com/app/apikey
2. Inicia sesión con tu cuenta de Google
3. Click en "Create API Key"
4. Copia la clave y pégala en `.env`

**OPCIONAL** (puedes dejar los valores por defecto):
```env
GEMINI_MODEL=gemini-flash-latest
LOG_LEVEL=INFO
SCRAPER_TIMEOUT=15
```

---

### 5. Verificar Instalación

Ejecuta el script de verificación:

```bash
python -c "from src.config import GEMINI_API_KEY; print('✅ Configuración OK' if GEMINI_API_KEY else '❌ Falta GEMINI_API_KEY')"
```

Si ves `✅ Configuración OK`, estás listo para continuar.

---

## 🧪 Prueba Inicial

### Ejecutar el Sistema

```bash
python main.py
```

**Qué esperar**:
1. Verás mensajes de log en consola
2. El sistema se conectará a los 3 portales activos
3. Buscará oportunidades con los triggers configurados
4. Analizará cada oportunidad con Gemini AI
5. Guardará resultados en `results_stage1.csv`
6. Al finalizar, presiona ENTER para salir

**Tiempo estimado**: 2-5 minutos (depende de la velocidad de internet y respuesta de portales)

---

## 📁 Estructura de Directorios

Después de la instalación, tu proyecto debería verse así:

```
MIA-V4.0/
│
├── .venv/                          # Entorno virtual (no subir a Git)
├── .env                            # Variables de entorno (no subir a Git)
├── .env.example                    # Plantilla de variables de entorno
├── .gitignore                      # Archivos ignorados por Git
│
├── config/                         # Archivos de configuración
│   └── prompts.json                # Plantillas de prompts para Gemini
│
├── src/                            # Código fuente
│   ├── __pycache__/                # Cache de Python (no subir a Git)
│   ├── analyzer.py                 # Módulo de análisis con IA
│   ├── config.py                   # Configuración centralizada
│   ├── scraper.py                  # Módulo de scraping
│   └── sheets_manager.py           # Módulo de salida de datos
│
├── main.py                         # Punto de entrada principal
├── requirements.txt                # Dependencias del proyecto
├── INSTALL.md                      # Esta guía
├── PLAN_IMPLEMENTACION.md          # Plan de desarrollo
├── DOCUMENTACION_ETAPAS_0_1.md     # Documentación técnica
│
├── historial_ejecuciones.txt       # Log de ejecuciones (generado)
└── results_stage1.csv              # Resultados (generado)
```

---

## 🔧 Configuración Avanzada

### Configurar Google Sheets (Opcional - Fase 4)

1. **Crear proyecto en Google Cloud Console**:
   - Visita: https://console.cloud.google.com
   - Crea un nuevo proyecto
   - Habilita "Google Sheets API"

2. **Crear credenciales**:
   - Ve a "Credenciales" → "Crear credenciales" → "Cuenta de servicio"
   - Descarga el archivo JSON de credenciales
   - Guárdalo como `data/service_account.json`

3. **Configurar en `.env`**:
   ```env
   GOOGLE_SHEETS_CREDENTIALS_PATH=data/service_account.json
   GOOGLE_SHEETS_SPREADSHEET_ID=tu_spreadsheet_id_aqui
   ```

4. **Compartir spreadsheet**:
   - Abre tu Google Sheet
   - Comparte con el email de la cuenta de servicio
   - Dale permisos de "Editor"

---

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'requests'"
**Solución**: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Error: "GEMINI_API_KEY not found in .env"
**Solución**: 
1. Verifica que el archivo `.env` existe
2. Verifica que `GEMINI_API_KEY=tu_clave` está en el archivo
3. Reinicia el programa

### Error: "ConnectionError" o "Timeout"
**Solución**:
1. Verifica tu conexión a internet
2. Aumenta el timeout en `.env`:
   ```env
   SCRAPER_TIMEOUT=30
   ```
3. Algunos portales pueden estar caídos temporalmente

### Error: "JSONDecodeError" en analyzer.py
**Solución**:
1. Gemini puede haber retornado respuesta inválida
2. Verifica que tu API key es correcta
3. Revisa el log para ver la respuesta de Gemini
4. El sistema continuará con las siguientes oportunidades

### El programa se cierra inmediatamente
**Solución**:
1. Ejecuta desde terminal/consola (no doble click)
2. Verifica que el entorno virtual está activado
3. Revisa `historial_ejecuciones.txt` para ver errores

---

## 📊 Verificar Resultados

### Archivo CSV
Abre `results_stage1.csv` con Excel, Google Sheets o un editor de texto.

**Columnas**:
- `Portal`: Nombre del portal donde se detectó
- `MIA_URL`: URL de la oportunidad
- `MIA_Keywords_Detectadas`: Triggers que activaron la detección
- `MIA_Rubro`: Clasificación por rubro (Purificación/Efluentes)
- `MIA_Score_IA`: Relevancia de 0-100
- `MIA_Resumen_Tecnico`: Resumen en español

### Archivo de Log
Abre `historial_ejecuciones.txt` para ver el historial completo de ejecuciones.

---

## 🔄 Actualizar el Sistema

### Actualizar código:
```bash
git pull origin main
```

### Actualizar dependencias:
```bash
pip install -r requirements.txt --upgrade
```

### Verificar cambios:
```bash
python main.py
```

---

## 🆘 Soporte

### Documentación
- **Técnica**: Ver `DOCUMENTACION_ETAPAS_0_1.md`
- **Plan de Desarrollo**: Ver `PLAN_IMPLEMENTACION.md`

### Contacto
- **Proyecto**: MIA V4.0
- **Empresa**: Water Tech S.A.

---

## ✅ Checklist de Instalación

- [ ] Python 3.9+ instalado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo `.env` creado y configurado
- [ ] GEMINI_API_KEY configurada
- [ ] Prueba inicial ejecutada exitosamente
- [ ] Archivo `results_stage1.csv` generado
- [ ] Log visible en `historial_ejecuciones.txt`

---

**¡Felicitaciones! 🎉 MIA V4.0 está instalado y listo para usar.**

Para próximos pasos, consulta `PLAN_IMPLEMENTACION.md`.
