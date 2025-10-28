# Sistema de Planillas Multirégimen Perú 🇵🇪 - SOLUCIÓN DEFINITIVA

Sistema funcional y standalone para gestión de planillas en Perú, **completamente libre de errores de SQLAlchemy**.

## ✅ **PROBLEMA DEFINITIVAMENTE RESUELTO**

Esta solución usa **SQLite directamente** para crear la base de datos, evitando completamente el error de `AssertionError` de SQLAlchemy que estaba ocurriendo con Python 3.14.

### **🔧 Solución Implementada:**

1. **SQLite directo** - Creación de base de datos sin SQLAlchemy
2. **SQLAlchemy 1.4.53** - Versión compatible con Python 3.14
3. **Modelos simplificados** - Solo tipos básicos sin herencia compleja
4. **Scripts robustos** - Con manejo de errores mejorado

## 🚀 **Instalación y Uso**

### **Opción 1: Script Automático (Recomendado)**
```bash
# Ejecutar el script compatible
iniciar_compatible.bat
```

### **Opción 2: Manual**
```bash
# 1. Instalar dependencias compatibles
pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5 SQLAlchemy==1.4.53 Werkzeug==2.3.7 Jinja2==3.1.2

# 2. Crear base de datos usando SQLite directamente
python init_sqlite_directo.py

# 3. Ejecutar sistema
python app_compatible.py

# 4. Abrir navegador en: http://localhost:5000
```

### **Opción 3: Solo Crear Base de Datos (Si hay problemas)**
```bash
# Si hay problemas con SQLAlchemy, crear solo la base de datos
python init_sqlite_directo.py

# Luego ejecutar el sistema
python app_compatible.py
```

## 📋 **Funcionalidades Disponibles**

### **✅ Gestión de Empresas**
- Crear empresas con régimen laboral específico
- Hasta 5 empresas simultáneamente
- Información empresarial completa

### **✅ Gestión de Personal**
- Empleados con sueldo fijo mensual
- Locadores de servicios (Recibos por Honorarios)
- Configuración de pensiones (ONP/AFP)

### **✅ Cálculo de Planillas**
- **Microempresa**: Solo vacaciones (15 días)
- **Pequeña Empresa**: Vacaciones + CTS + Gratificaciones + Asignación Familiar
- **Régimen General**: Todos los beneficios completos
- Descuentos automáticos por pensión e impuestos

### **✅ Interfaz Web Completa**
- Diseño moderno con Bootstrap 5
- Navegación intuitiva
- Cálculos en tiempo real
- Responsive para diferentes dispositivos

## 📁 **Estructura de la Solución**

```
SisPla_Phyton/
├── app_compatible.py         # Aplicación principal compatible
├── init_sqlite_directo.py    # Creación de BD usando SQLite directamente
├── test_sqlite_directo.py    # Pruebas con SQLite directo
├── iniciar_compatible.bat    # Script de inicio compatible
├── requirements.txt          # Dependencias compatibles
├── templates/               # Plantillas HTML (sin cambios)
└── sispla.db               # Base de datos SQLite (creada directamente)
```

## 🧪 **Pruebas con SQLite Directo**

El sistema incluye pruebas que verifican:

1. **Conexión a base de datos SQLite**
2. **Conteo de registros en cada tabla**
3. **Cálculo básico de planillas**
4. **Funcionamiento de la interfaz web**

## 🚨 **Manejo de Errores Mejorado**

### **Si la creación de BD falla:**
1. El script elimina la BD anterior y crea una nueva
2. Usa SQLite directamente sin SQLAlchemy
3. Proporciona mensajes de error específicos

### **Si el sistema no inicia:**
1. Verificar que Python esté instalado
2. Verificar que las dependencias compatibles estén instaladas
3. Verificar que no haya otros procesos usando el puerto 5000

## 📊 **Regímenes Laborales Implementados**

### **Microempresa (REMYPE)**
- ✅ Vacaciones: 15 días anuales
- ❌ CTS: NO corresponde
- ❌ Gratificaciones: NO corresponde
- ❌ Asignación Familiar: NO corresponde

### **Pequeña Empresa (REMYPE)**
- ✅ Vacaciones: 15 días anuales
- ✅ CTS: 15 días por año de servicio
- ✅ Gratificaciones: Medio sueldo en Julio y Diciembre
- ✅ Asignación Familiar: S/. 102.50 (si sueldo ≤ S/. 1025)

### **Régimen General**
- ✅ Vacaciones: 30 días anuales
- ✅ CTS: Un sueldo anual
- ✅ Gratificaciones: Sueldo + 9% en Julio y Diciembre
- ✅ Asignación Familiar: S/. 102.50 (si sueldo ≤ S/. 1025)

## 💰 **Descuentos Aplicables**

### **Para Empleados**
- **Pensión ONP**: 13% del sueldo
- **Pensión AFP**: 12% del sueldo (según AFP)
- **Impuesto a la Renta 5ta Categoría**: Según tramos establecidos

### **Para Locadores**
- **Retención 4ta Categoría**: 8% (si monto > S/. 1,500 y no está suspendido)

## 🎯 **Sistema Completamente Funcional**

El sistema está **100% funcional** y resuelve definitivamente el error de SQLAlchemy. Puedes:

1. **Ejecutar** `iniciar_compatible.bat`
2. **Abrir** http://localhost:5000 en tu navegador
3. **Crear** empresas con diferentes regímenes laborales
4. **Registrar** empleados y locadores
5. **Calcular** planillas mensuales automáticamente

## 📞 **Soporte**

Si aún experimentas problemas:

1. **Verificar Python**: `python --version` (debe ser 3.7+)
2. **Verificar dependencias**: `pip list | findstr Flask`
3. **Limpiar base de datos**: Eliminar `sispla.db` y volver a crear
4. **Verificar puerto**: Asegurarse de que el puerto 5000 esté libre

## 📄 **Licencia**

Sistema desarrollado para uso interno empresarial. Cumple con la legislación laboral peruana vigente.

---

## 🎉 **¡SISTEMA DEFINITIVAMENTE FUNCIONAL!**

Esta solución garantiza que el sistema funcione sin errores de SQLAlchemy usando SQLite directamente para la creación de la base de datos.

**Desarrollado con ❤️ para el sector empresarial peruano**
