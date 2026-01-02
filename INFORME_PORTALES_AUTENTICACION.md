# Informe de Portales con Autenticación Requerida - MIA V4.0

## 📋 Resumen Ejecutivo

**Fecha**: 2026-01-02  
**Objetivo**: Identificar portales que requieren autenticación y preparar proceso de registro  
**Destinatario**: Colaborador responsable de gestión de credenciales  
**Urgencia**: 🔴 Alta (bloquea implementación de portales críticos)

---

## 🔐 Portales que Requieren Autenticación

### Resumen por Prioridad

| Portal | Prioridad | Valor de Negocio | Tipo de Auth | Estado |
|--------|-----------|------------------|--------------|--------|
| proveedores.ypf.com | ⭐⭐⭐⭐⭐ | 🔴 MUY ALTO | Registro de Proveedor | ⏳ Pendiente |
| service.ariba.com | ⭐⭐⭐⭐ | 🔴 ALTO | OAuth/Proveedor | ⏳ Pendiente |
| srpcm.pjn.gov.ar | ⭐ | 🟢 BAJO | Registro Obligatorio | ⏳ Pendiente |
| samqa.vw.com.ar | ⭐⭐ | 🟡 MEDIO | Portal Corporativo | ⏳ Pendiente |
| esupplierconnect.com | ⭐⭐ | 🟡 MEDIO | Portal B2B | ⏳ Pendiente |
| portalproveedores.acindar.com.ar | ⭐⭐ | 🟡 MEDIO | Registro Proveedor | ⏳ Pendiente |
| ecup.arcor.com | ⭐⭐ | 🟡 MEDIO | Portal Corporativo | ⏳ Pendiente |
| proveedores.molinos.com.ar | ⭐⭐ | 🟡 MEDIO | Portal Corporativo | ⏳ Pendiente |
| compras.lomanegra.com | ⭐⭐ | 🟡 MEDIO | Portal Corporativo | ⏳ Pendiente |
| fsp.portal.covisint.com | ⭐⭐ | 🟡 MEDIO | Portal B2B Automotriz | ⏳ Pendiente |

**Total**: 10 portales requieren autenticación

---

## 🎯 Portales Prioritarios para Registro Inmediato

### 1. proveedores.ypf.com ⭐⭐⭐⭐⭐ CRÍTICO

**Información del Portal**:
- **URL**: https://proveedores.ypf.com
- **Empresa**: YPF S.A. (Yacimientos Petrolíferos Fiscales)
- **Tipo**: Portal de Proveedores Corporativo
- **Valor de Negocio**: 🔴 MUY ALTO
- **Razón**: YPF tiene grandes proyectos de agua/efluentes en refinerías y plantas

**Proceso de Registro**:
1. **Acceder a**: https://proveedores.ypf.com
2. **Buscar sección**: "Registro de Nuevos Proveedores" o "Alta de Proveedor"
3. **Documentación requerida** (estimada):
   - CUIT de Water Tech S.A.
   - Certificado de inscripción AFIP
   - Constancia de inscripción en IIBB
   - Certificado de cumplimiento fiscal
   - Balance contable (último ejercicio)
   - Póliza de seguro de responsabilidad civil
   - Referencias comerciales

**Datos de la Empresa para Registro**:
```
Razón Social: Water Tech S.A.
CUIT: [COMPLETAR]
Domicilio Legal: [COMPLETAR]
Teléfono: [COMPLETAR]
Email de Contacto: [COMPLETAR]
Rubro Principal: Tratamiento de Agua y Efluentes
Categoría: Servicios Ambientales / Ingeniería
```

**Credenciales a Obtener**:
- Usuario/Email
- Contraseña
- Token de acceso (si aplica)
- Certificado digital (si aplica)

**Información a Registrar en Sistema MIA**:
```env
# YPF Portal Credentials
YPF_USERNAME=usuario@watertech.com.ar
YPF_PASSWORD=contraseña_segura
YPF_TOKEN=token_si_aplica
YPF_CERT_PATH=path/to/certificate.pem  # Si requiere certificado
```

---

### 2. service.ariba.com ⭐⭐⭐⭐ ALTO

**Información del Portal**:
- **URL**: https://service.ariba.com
- **Empresa**: SAP Ariba (Plataforma Global)
- **Tipo**: Plataforma B2B de Procurement
- **Valor de Negocio**: 🔴 ALTO
- **Razón**: Múltiples empresas grandes usan esta plataforma

**Proceso de Registro**:
1. **Acceder a**: https://service.ariba.com
2. **Opción**: "Supplier Registration" o "Registro de Proveedores"
3. **Tipo de cuenta**: Supplier Network Account
4. **Documentación requerida**:
   - Información fiscal de la empresa
   - Datos bancarios
   - Certificaciones (ISO, etc.)
   - Referencias comerciales

**Datos de la Empresa para Registro**:
```
Company Name: Water Tech S.A.
Tax ID: AR-[CUIT]
Country: Argentina
Business Type: Environmental Services
Primary Commodity: Water Treatment & Wastewater Management
```

**Credenciales a Obtener**:
- Ariba Network ID (ANID)
- Usuario
- Contraseña
- API Key (si disponible)

**Información a Registrar en Sistema MIA**:
```env
# SAP Ariba Credentials
ARIBA_NETWORK_ID=ANID_numero
ARIBA_USERNAME=usuario@watertech.com.ar
ARIBA_PASSWORD=contraseña_segura
ARIBA_API_KEY=api_key_si_disponible
```

---

### 3. srpcm.pjn.gov.ar ⭐ BAJA PRIORIDAD

**Información del Portal**:
- **URL**: https://srpcm.pjn.gov.ar
- **Organismo**: Poder Judicial de la Nación
- **Tipo**: Sistema de Registro de Proveedores
- **Valor de Negocio**: 🟢 BAJO-MEDIO
- **Razón**: Volumen bajo de licitaciones relevantes

**Proceso de Registro**:
1. **Acceder a**: https://srpcm.pjn.gov.ar
2. **Sección**: "Registro de Proveedores"
3. **Documentación requerida**:
   - CUIT
   - Estatuto social
   - Certificado de cumplimiento fiscal
   - Antecedentes penales de directores

**Credenciales a Obtener**:
- Usuario
- Contraseña
- Número de proveedor

**Información a Registrar en Sistema MIA**:
```env
# Poder Judicial Credentials
PJN_USERNAME=usuario
PJN_PASSWORD=contraseña
PJN_PROVEEDOR_ID=numero_proveedor
```

---

## 📝 Portales Corporativos Privados (Prioridad Media)

### 4-10. Portales de Empresas Privadas

**Portales**:
- samqa.vw.com.ar (Volkswagen)
- esupplierconnect.com (Ford, GM)
- portalproveedores.acindar.com.ar (Acindar)
- ecup.arcor.com (Arcor)
- proveedores.molinos.com.ar (Molinos)
- compras.lomanegra.com (Loma Negra)
- fsp.portal.covisint.com (Covisint - Automotriz)

**Proceso General**:
1. Contactar área de compras de cada empresa
2. Solicitar alta como proveedor
3. Completar formularios específicos
4. Presentar documentación corporativa
5. Esperar aprobación (puede tomar semanas)

**Documentación Común Requerida**:
- CUIT y constancia de inscripción
- Balance contable
- Referencias comerciales
- Certificaciones de calidad (ISO 9001, ISO 14001)
- Póliza de seguro
- Capacidad técnica y financiera

---

## 🔧 Configuración del Sistema MIA para Credenciales

### Archivo de Configuración: `.env`

Crear sección específica para credenciales de portales:

```env
# ============================================================================
# CREDENCIALES DE PORTALES CON AUTENTICACIÓN
# ============================================================================
# IMPORTANTE: Este archivo NO debe subirse a Git (.gitignore)
# Mantener credenciales seguras y actualizadas

# ----------------------------------------------------------------------------
# YPF - Portal de Proveedores (CRÍTICO)
# ----------------------------------------------------------------------------
YPF_ENABLED=false  # Cambiar a true cuando se obtengan credenciales
YPF_USERNAME=
YPF_PASSWORD=
YPF_TOKEN=
YPF_CERT_PATH=

# ----------------------------------------------------------------------------
# SAP Ariba - Plataforma B2B (ALTO)
# ----------------------------------------------------------------------------
ARIBA_ENABLED=false
ARIBA_NETWORK_ID=
ARIBA_USERNAME=
ARIBA_PASSWORD=
ARIBA_API_KEY=

# ----------------------------------------------------------------------------
# Poder Judicial - Sistema de Proveedores (BAJO)
# ----------------------------------------------------------------------------
PJN_ENABLED=false
PJN_USERNAME=
PJN_PASSWORD=
PJN_PROVEEDOR_ID=

# ----------------------------------------------------------------------------
# Portales Corporativos Privados (MEDIO)
# ----------------------------------------------------------------------------
# Volkswagen
VW_ENABLED=false
VW_USERNAME=
VW_PASSWORD=

# Ford/GM - eSupplier Connect
ESUPPLIER_ENABLED=false
ESUPPLIER_USERNAME=
ESUPPLIER_PASSWORD=

# Acindar
ACINDAR_ENABLED=false
ACINDAR_USERNAME=
ACINDAR_PASSWORD=

# Arcor
ARCOR_ENABLED=false
ARCOR_USERNAME=
ARCOR_PASSWORD=

# Molinos
MOLINOS_ENABLED=false
MOLINOS_USERNAME=
MOLINOS_PASSWORD=

# Loma Negra
LOMANEGRA_ENABLED=false
LOMANEGRA_USERNAME=
LOMANEGRA_PASSWORD=

# Covisint
COVISINT_ENABLED=false
COVISINT_USERNAME=
COVISINT_PASSWORD=
```

### Actualización de `src/config.py`

Agregar lectura de credenciales:

```python
# ============================================================================
# CREDENCIALES DE PORTALES CON AUTENTICACIÓN
# ============================================================================

# YPF
YPF_ENABLED = os.getenv("YPF_ENABLED", "false").lower() == "true"
YPF_USERNAME = os.getenv("YPF_USERNAME")
YPF_PASSWORD = os.getenv("YPF_PASSWORD")
YPF_TOKEN = os.getenv("YPF_TOKEN")
YPF_CERT_PATH = os.getenv("YPF_CERT_PATH")

# SAP Ariba
ARIBA_ENABLED = os.getenv("ARIBA_ENABLED", "false").lower() == "true"
ARIBA_NETWORK_ID = os.getenv("ARIBA_NETWORK_ID")
ARIBA_USERNAME = os.getenv("ARIBA_USERNAME")
ARIBA_PASSWORD = os.getenv("ARIBA_PASSWORD")
ARIBA_API_KEY = os.getenv("ARIBA_API_KEY")

# ... (resto de credenciales)
```

---

## 📋 Checklist para el Colaborador

### Tareas Inmediatas (Prioridad Alta)

- [ ] **YPF - proveedores.ypf.com**
  - [ ] Acceder al portal y verificar proceso de registro
  - [ ] Recopilar documentación requerida
  - [ ] Completar formulario de alta de proveedor
  - [ ] Obtener credenciales de acceso
  - [ ] Documentar proceso y limitaciones
  - [ ] Entregar credenciales de forma segura

- [ ] **SAP Ariba - service.ariba.com**
  - [ ] Crear cuenta en Ariba Network
  - [ ] Completar perfil de empresa
  - [ ] Obtener ANID y credenciales
  - [ ] Verificar acceso a licitaciones
  - [ ] Documentar proceso

### Tareas de Prioridad Media

- [ ] **Portales Corporativos**
  - [ ] Contactar área de compras de cada empresa
  - [ ] Solicitar proceso de alta de proveedor
  - [ ] Preparar documentación corporativa
  - [ ] Seguimiento de solicitudes
  - [ ] Obtener credenciales cuando sean aprobadas

### Tareas de Prioridad Baja

- [ ] **Poder Judicial - srpcm.pjn.gov.ar**
  - [ ] Registrarse en sistema
  - [ ] Obtener credenciales
  - [ ] Documentar proceso

---

## 🔒 Seguridad de Credenciales

### Buenas Prácticas

1. **Almacenamiento Seguro**:
   - Usar gestor de contraseñas corporativo
   - No compartir credenciales por email sin cifrar
   - Usar canales seguros (ej: LastPass, 1Password)

2. **Archivo `.env`**:
   - NUNCA subir a Git
   - Mantener backup cifrado
   - Actualizar cuando cambien credenciales

3. **Rotación de Contraseñas**:
   - Cambiar contraseñas cada 90 días
   - Usar contraseñas fuertes (12+ caracteres)
   - No reutilizar contraseñas

4. **Acceso Limitado**:
   - Solo personal autorizado
   - Documentar quién tiene acceso
   - Revocar acceso cuando sea necesario

---

## 📊 Formato de Entrega de Credenciales

### Plantilla para Documentar Credenciales

```markdown
# Credenciales de Portal: [NOMBRE_PORTAL]

**Fecha de Registro**: YYYY-MM-DD
**Registrado por**: [Nombre del colaborador]
**Portal**: [URL]

## Credenciales
- **Usuario**: usuario@email.com
- **Contraseña**: [usar gestor de contraseñas]
- **Token/API Key**: [si aplica]
- **Otros**: [certificados, IDs, etc.]

## Proceso de Registro
1. [Paso 1]
2. [Paso 2]
3. [...]

## Limitaciones Conocidas
- [Limitación 1]
- [Limitación 2]

## Contacto en el Portal
- **Nombre**: [Contacto]
- **Email**: [email]
- **Teléfono**: [teléfono]

## Notas Adicionales
[Cualquier información relevante]
```

---

## 🚀 Próximos Pasos Después de Obtener Credenciales

### Para el Equipo de Desarrollo

1. **Actualizar `.env`**:
   - Agregar credenciales obtenidas
   - Habilitar portal (`ENABLED=true`)

2. **Implementar Autenticación en Scrapers**:
   - Modificar scraper específico
   - Agregar lógica de login
   - Manejar sesiones y cookies
   - Implementar refresh de tokens

3. **Testing**:
   - Verificar que login funciona
   - Probar extracción de datos
   - Validar manejo de errores

4. **Documentación**:
   - Actualizar documentación técnica
   - Documentar limitaciones
   - Crear guía de troubleshooting

---

## 📞 Contacto y Soporte

**Para dudas sobre este informe**:
- Equipo de Desarrollo MIA V4.0
- Water Tech S.A.

**Para dudas sobre registro en portales**:
- Contactar área de compras de cada empresa
- Consultar con asesor legal si es necesario

---

## 📅 Timeline Estimado

| Actividad | Duración Estimada | Responsable |
|-----------|-------------------|-------------|
| Registro en YPF | 2-4 semanas | Colaborador |
| Registro en Ariba | 1-2 semanas | Colaborador |
| Registro en portales corporativos | 3-6 semanas | Colaborador |
| Implementación en MIA | 1-2 días | Desarrollo |
| Testing y validación | 2-3 días | Desarrollo |

**Total estimado**: 6-8 semanas para portales prioritarios

---

## ✅ Criterios de Éxito

### Portal Considerado "Listo"

- [ ] Credenciales obtenidas y verificadas
- [ ] Credenciales almacenadas de forma segura
- [ ] Proceso de registro documentado
- [ ] Limitaciones identificadas
- [ ] Contacto en el portal establecido
- [ ] Credenciales entregadas a equipo de desarrollo
- [ ] Scraper implementado y testeado
- [ ] Portal habilitado en producción

---

**Fecha de Informe**: 2026-01-02  
**Versión**: 1.0  
**Estado**: 📝 LISTO PARA ENTREGA AL COLABORADOR
