# Sistema de Planillas Multirégimen Perú 🇵🇪 - VERSIÓN MEJORADA

Sistema funcional y standalone para gestión de planillas en Perú, **con todas las mejoras solicitadas implementadas**.

## ✅ **MEJORAS IMPLEMENTADAS**

### **🏦 Campos Bancarios Agregados**
- ✅ **Cuenta bancaria** para empleados y locadores
- ✅ **Selección de banco** principal (BCP, BBVA, Scotiabank, etc.)
- ✅ **Información bancaria visible** en planillas
- ✅ **Templates actualizados** con nuevos campos

### **💰 Pago Quincenal Implementado**
- ✅ **Tipo de pago**: Mensual (100%) o Quincenal (50%)
- ✅ **Cálculo automático** según tipo seleccionado
- ✅ **Interfaz intuitiva** para seleccionar tipo de pago
- ✅ **Información visible** en planillas con badges

### **📊 Conteo Corregido**
- ✅ **Solo cuenta empleados activos** en ventana inicial
- ✅ **Solo cuenta locadores activos** en ventana inicial
- ✅ **Conteo preciso** usando filtros de estado
- ✅ **Información actualizada** en tiempo real

### **📖 Manual de Funcionamiento**
- ✅ **Documentación completa** del cálculo de planilla
- ✅ **Ejemplos paso a paso** con casos reales
- ✅ **Explicación detallada** de todos los regímenes laborales
- ✅ **Guía de configuración** y parámetros del sistema

## 🚀 **Instalación y Uso**

### **Opción 1: Script Automático (Recomendado)**
```bash
# Ejecutar el script mejorado
iniciar_mejorado.bat
```

### **Opción 2: Manual**
```bash
# 1. Instalar dependencias compatibles
pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5 SQLAlchemy==1.4.53 Werkzeug==2.3.7 Jinja2==3.1.2

# 2. Actualizar base de datos existente
python actualizar_bd.py
python actualizar_campos_bancarios.py

# 3. Probar rutas del sistema
python test_rutas.py

# 4. Ejecutar sistema
python app_compatible.py

# 5. Abrir navegador en: http://localhost:5000
```

## 📁 **Estructura Actualizada del Proyecto**

```
SisPla_Phyton/
├── app_compatible.py              # Aplicación principal con mejoras
├── actualizar_bd.py               # Actualización de tablas
├── actualizar_campos_bancarios.py # Actualización de campos bancarios
├── init_sqlite_directo.py         # Creación de BD completa
├── test_rutas.py                  # Pruebas del sistema
├── iniciar_mejorado.bat           # Script de inicio mejorado
├── MANUAL_CALCULO_PLANILLA.md     # Manual completo de funcionamiento
├── requirements.txt               # Dependencias compatibles
├── templates/                     # Plantillas HTML actualizadas
│   ├── base.html
│   ├── index.html
│   ├── empresas.html              # ✅ Conteo corregido
│   ├── nueva_empresa.html
│   ├── personal.html
│   ├── nuevo_empleado.html        # ✅ Campos bancarios agregados
│   ├── nuevo_locador.html         # ✅ Campos bancarios agregados
│   ├── planilla.html              # ✅ Tipo de pago visible
│   ├── ausencias.html
│   ├── nueva_ausencia.html
│   ├── deudas.html
│   ├── nuevo_prestamo.html
│   └── nuevo_adelanto.html
└── sispla.db                      # Base de datos SQLite actualizada
```

## 🏦 **Bancos Soportados**

- **Banco de Crédito del Perú (BCP)**
- **BBVA Continental**
- **Scotiabank**
- **Interbank**
- **BanBif**
- **Banco Pichincha**
- **Otro**

## 💰 **Tipos de Pago Implementados**

### **Pago Mensual (100%)**
- Sueldo completo según días trabajados
- Beneficios sociales completos
- Descuentos proporcionales

### **Pago Quincenal (50%)**
- 50% del sueldo según días trabajados
- Beneficios sociales proporcionales
- Descuentos proporcionales

## 📊 **Regímenes Laborales Completos**

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

## 🧮 **Cálculo de Planilla Mejorado**

### **Proceso Completo:**
1. **Días trabajados** - Considerando ausencias
2. **Sueldo ajustado** - Proporcional a días trabajados
3. **Tipo de pago** - Mensual (100%) o Quincenal (50%)
4. **Beneficios sociales** - Según régimen laboral
5. **Descuentos automáticos** - Pensión, impuestos, deudas
6. **Neto a pagar** - Con información bancaria

### **Información Bancaria Visible:**
- Banco seleccionado
- Número de cuenta
- Tipo de pago aplicado
- Datos para transferencias

## 📖 **Manual de Funcionamiento**

El archivo `MANUAL_CALCULO_PLANILLA.md` incluye:

- **Explicación detallada** de cada régimen laboral
- **Cálculo paso a paso** con ejemplos reales
- **Control de ausencias** y su impacto
- **Gestión de deudas internas**
- **Configuración del sistema**
- **Reportes disponibles**
- **Consideraciones legales**

## 🧪 **Pruebas del Sistema**

El sistema incluye pruebas completas que verifican:

1. **Creación de base de datos** con todas las tablas
2. **Inserción de datos** con campos bancarios
3. **Funcionamiento de todas las rutas**
4. **Cálculo de planillas** con tipo de pago
5. **Gestión de ausencias** y deudas
6. **Conteo correcto** de empleados activos

## 🎯 **Flujo de Trabajo Completo**

### **1. Configuración Inicial**
1. Crear empresas con régimen laboral específico
2. Registrar empleados con información bancaria
3. Configurar tipo de pago (mensual/quincenal)
4. Registrar locadores con datos bancarios

### **2. Gestión Mensual**
1. Registrar ausencias (faltas, permisos, vacaciones)
2. Crear préstamos y adelantos según necesidad
3. Calcular planillas mensuales automáticamente
4. Verificar información bancaria para transferencias

### **3. Cálculo Automático Mejorado**
1. El sistema calcula días trabajados considerando ausencias
2. Aplica tipo de pago (mensual/quincenal)
3. Calcula beneficios según régimen laboral
4. Descuenta automáticamente pensiones e impuestos
5. Descuenta automáticamente préstamos y adelantos
6. Genera planilla final con datos bancarios

## 📞 **Soporte**

Si experimentas problemas:

1. **Verificar Python**: `python --version` (debe ser 3.7+)
2. **Verificar dependencias**: `pip list | findstr Flask`
3. **Ejecutar pruebas**: `python test_rutas.py`
4. **Consultar manual**: `MANUAL_CALCULO_PLANILLA.md`
5. **Verificar puerto**: Asegurarse de que el puerto 5000 esté libre

## 📄 **Licencia**

Sistema desarrollado para uso interno empresarial. Cumple con la legislación laboral peruana vigente.

---

## 🎉 **¡SISTEMA COMPLETAMENTE MEJORADO!**

El sistema ahora incluye **todas las mejoras solicitadas**:

- ✅ **Campos bancarios** para empleados y locadores
- ✅ **Pago quincenal** (50% del sueldo)
- ✅ **Conteo corregido** de empleados activos
- ✅ **Manual completo** de funcionamiento
- ✅ **Interfaz mejorada** con información bancaria
- ✅ **Cálculos automáticos** con tipo de pago

**Desarrollado con ❤️ para el sector empresarial peruano**
