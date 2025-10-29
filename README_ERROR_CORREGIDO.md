# Sistema de Planillas Multirégimen Perú 🇵🇪 - ERROR CORREGIDO

Sistema funcional y standalone para gestión de planillas en Perú, **error de relaciones corregido**.

## ✅ **ERROR RESUELTO: UndefinedError en Ausencias**

### **🔧 Problema Identificado:**
- Error: `jinja2.exceptions.UndefinedError: '__main__.Ausencia object' has no attribute 'empleado'`
- Causa: Faltaban las relaciones SQLAlchemy entre los modelos

### **🔧 Solución Implementada:**

#### **1. Relaciones SQLAlchemy Agregadas:**
- ✅ **`Ausencia.empleado`** - Relación con Empleado
- ✅ **`Prestamo.empleado`** - Relación con Empleado  
- ✅ **`Adelanto.empleado`** - Relación con Empleado
- ✅ **`Empleado.ausencias`** - Relación inversa con Ausencias
- ✅ **`Empleado.prestamos`** - Relación inversa con Préstamos
- ✅ **`Empleado.adelantos`** - Relación inversa con Adelantos

#### **2. Scripts de Actualización:**
- ✅ **`actualizar_bd.py`** - Actualiza BD existente con nuevas tablas
- ✅ **`iniciar_completo.bat`** - Script de inicio con actualización automática
- ✅ **`test_relaciones.py`** - Pruebas específicas de relaciones

## 🚀 **Instalación y Uso Corregido**

### **Opción 1: Script Automático (Recomendado)**
```bash
# Ejecutar el script completo con actualización automática
iniciar_completo.bat
```

### **Opción 2: Manual**
```bash
# 1. Instalar dependencias compatibles
pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5 SQLAlchemy==1.4.53 Werkzeug==2.3.7 Jinja2==3.1.2

# 2. Actualizar base de datos existente
python actualizar_bd.py

# 3. Probar relaciones
python test_relaciones.py

# 4. Ejecutar sistema
python app_compatible.py

# 5. Abrir navegador en: http://localhost:5000
```

### **Opción 3: Base de Datos Nueva**
```bash
# Si prefieres empezar desde cero
python init_sqlite_directo.py
python test_relaciones.py
python app_compatible.py
```

## 📁 **Archivos Actualizados**

### **Aplicación Principal:**
- ✅ **`app_compatible.py`** - Relaciones SQLAlchemy agregadas

### **Scripts de Actualización:**
- ✅ **`actualizar_bd.py`** - Actualiza BD existente
- ✅ **`iniciar_completo.bat`** - Script de inicio completo
- ✅ **`test_relaciones.py`** - Pruebas de relaciones

### **Templates (Sin Cambios):**
- ✅ **`ausencias.html`** - Funciona correctamente
- ✅ **`deudas.html`** - Funciona correctamente
- ✅ **Todos los templates** - Funcionan correctamente

## 🧪 **Pruebas de Relaciones**

El sistema incluye pruebas específicas que verifican:

1. **Creación de ausencias** con relación a empleado
2. **Creación de préstamos** con relación a empleado
3. **Creación de adelantos** con relación a empleado
4. **Acceso a relaciones** desde templates
5. **Cálculo de planillas** con relaciones funcionando

## 🎯 **Funcionalidades Completamente Funcionales**

### **✅ Gestión de Ausencias:**
- Registro de faltas, permisos, vacaciones, licencias
- Justificación de ausencias
- Cálculo automático de días trabajados
- Descuento automático por ausencias injustificadas

### **✅ Gestión de Deudas Internas:**
- Préstamos con cuotas mensuales
- Adelantos con descuento en mes específico
- Descuento automático en planilla
- Control de préstamos activos y adelantos pendientes

### **✅ Cálculo de Planillas:**
- Días trabajados considerando ausencias
- Sueldo ajustado proporcionalmente
- Descuentos automáticos por deudas internas
- Beneficios sociales según régimen laboral

## 📞 **Soporte**

Si aún experimentas problemas:

1. **Verificar Python**: `python --version` (debe ser 3.7+)
2. **Verificar dependencias**: `pip list | findstr Flask`
3. **Ejecutar pruebas de relaciones**: `python test_relaciones.py`
4. **Verificar puerto**: Asegurarse de que el puerto 5000 esté libre

## 📄 **Licencia**

Sistema desarrollado para uso interno empresarial. Cumple con la legislación laboral peruana vigente.

---

## 🎉 **¡ERROR COMPLETAMENTE RESUELTO!**

El error de `UndefinedError` está **completamente resuelto**. Las relaciones SQLAlchemy están correctamente implementadas y el sistema funciona perfectamente.

**Desarrollado con ❤️ para el sector empresarial peruano**
