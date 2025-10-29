# Sistema de Planillas Multirégimen Perú 🇵🇪 - COMPLETO

Sistema funcional y standalone para gestión de planillas en Perú, **completamente funcional** con todas las funcionalidades implementadas.

## ✅ **FUNCIONALIDADES COMPLETAMENTE IMPLEMENTADAS**

### **🏢 Gestión de Empresas**
- ✅ Crear hasta 5 empresas simultáneamente
- ✅ Configurar régimen laboral por empresa
- ✅ Gestión de información empresarial completa

### **👥 Gestión de Personal**
- ✅ Empleados con sueldo fijo mensual
- ✅ Locadores de servicios (Recibos por Honorarios)
- ✅ Configuración de pensiones (ONP/AFP)
- ✅ Control de estado activo/inactivo

### **📅 Control de Ausencias**
- ✅ Registro de faltas, permisos, vacaciones y licencias
- ✅ Justificación de ausencias
- ✅ Cálculo automático de días trabajados
- ✅ Descuento automático por ausencias injustificadas

### **💰 Gestión de Deudas Internas**
- ✅ Préstamos con cuotas mensuales
- ✅ Adelantos con descuento en mes específico
- ✅ Descuento automático en planilla
- ✅ Control de préstamos activos y adelantos pendientes

### **🧮 Cálculo de Planillas**
- ✅ **Microempresa**: Solo vacaciones (15 días)
- ✅ **Pequeña Empresa**: Vacaciones + CTS + Gratificaciones + Asignación Familiar
- ✅ **Régimen General**: Todos los beneficios completos
- ✅ Descuentos automáticos por pensión e impuestos
- ✅ Descuentos automáticos por ausencias
- ✅ Descuentos automáticos por deudas internas

### **🌐 Interfaz Web Completa**
- ✅ Diseño moderno con Bootstrap 5
- ✅ Navegación intuitiva
- ✅ Cálculos en tiempo real
- ✅ Responsive para diferentes dispositivos

## 🚀 **Instalación y Uso**

### **Opción 1: Script Automático (Recomendado)**
```bash
# Simplemente ejecutar:
iniciar_compatible.bat
```

### **Opción 2: Manual**
```bash
# 1. Instalar dependencias compatibles
pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5 SQLAlchemy==1.4.53 Werkzeug==2.3.7 Jinja2==3.1.2

# 2. Crear base de datos usando SQLite directamente
python init_sqlite_directo.py

# 3. Probar rutas del sistema
python test_rutas.py

# 4. Ejecutar sistema
python app_compatible.py

# 5. Abrir navegador en: http://localhost:5000
```

## 📁 **Estructura Completa del Proyecto**

```
SisPla_Phyton/
├── app_compatible.py         # Aplicación principal completa
├── init_sqlite_directo.py    # Creación de BD con todas las tablas
├── test_rutas.py            # Pruebas completas del sistema
├── iniciar_compatible.bat    # Script de inicio completo
├── requirements.txt          # Dependencias compatibles
├── templates/               # Plantillas HTML completas
│   ├── base.html
│   ├── index.html
│   ├── empresas.html
│   ├── nueva_empresa.html
│   ├── personal.html
│   ├── nuevo_empleado.html
│   ├── nuevo_locador.html
│   ├── planilla.html
│   ├── ausencias.html       # ✅ NUEVO
│   ├── nueva_ausencia.html  # ✅ NUEVO
│   ├── deudas.html          # ✅ NUEVO
│   ├── nuevo_prestamo.html  # ✅ NUEVO
│   └── nuevo_adelanto.html  # ✅ NUEVO
└── sispla.db               # Base de datos SQLite completa
```

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
- **Préstamos**: Cuota mensual automática
- **Adelantos**: Descuento en mes específico
- **Ausencias**: Descuento proporcional por días faltados

### **Para Locadores**
- **Retención 4ta Categoría**: 8% (si monto > S/. 1,500 y no está suspendido)

## 🧪 **Pruebas del Sistema**

El sistema incluye pruebas completas que verifican:

1. **Creación de base de datos SQLite**
2. **Inserción de datos de ejemplo**
3. **Funcionamiento de todas las rutas**
4. **Cálculo de planillas con todos los descuentos**
5. **Gestión de ausencias**
6. **Gestión de deudas internas**
7. **Funcionamiento de la interfaz web**

## 🎯 **Flujo de Trabajo Completo**

### **1. Configuración Inicial**
1. Crear empresas con diferentes regímenes laborales
2. Registrar empleados y locadores
3. Configurar pensiones (ONP/AFP)

### **2. Gestión Mensual**
1. Registrar ausencias (faltas, permisos, vacaciones)
2. Crear préstamos y adelantos según necesidad
3. Calcular planillas mensuales automáticamente

### **3. Cálculo Automático**
1. El sistema calcula días trabajados considerando ausencias
2. Aplica beneficios según régimen laboral
3. Descuenta automáticamente pensiones e impuestos
4. Descuenta automáticamente préstamos y adelantos
5. Genera planilla final con neto a pagar

## 📞 **Soporte**

Si experimentas problemas:

1. **Verificar Python**: `python --version` (debe ser 3.7+)
2. **Verificar dependencias**: `pip list | findstr Flask`
3. **Ejecutar pruebas**: `python test_rutas.py`
4. **Verificar puerto**: Asegurarse de que el puerto 5000 esté libre

## 📄 **Licencia**

Sistema desarrollado para uso interno empresarial. Cumple con la legislación laboral peruana vigente.

---

## 🎉 **¡SISTEMA COMPLETAMENTE FUNCIONAL!**

El sistema está **100% funcional** con todas las funcionalidades implementadas:

- ✅ **Gestión de empresas** con diferentes regímenes laborales
- ✅ **Gestión de personal** (empleados y locadores)
- ✅ **Control de ausencias** con descuentos automáticos
- ✅ **Gestión de deudas internas** (préstamos y adelantos)
- ✅ **Cálculo de planillas** con todos los beneficios y descuentos
- ✅ **Interfaz web completa** y responsive

**Desarrollado con ❤️ para el sector empresarial peruano**
