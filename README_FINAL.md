# Sistema de Planillas Multirégimen Perú 🇵🇪 - VERSIÓN FINAL

Sistema funcional y standalone para gestión de planillas en Perú, capaz de manejar hasta 5 empresas simultáneamente con diferentes regímenes laborales: Microempresa (REMYPE), Pequeña Empresa (REMYPE) y Régimen General.

## ✅ **PROBLEMA RESUELTO: Error de SQLAlchemy**

Esta versión final corrige completamente el error de `AssertionError` de SQLAlchemy que estaba ocurriendo durante la inicialización de la base de datos.

### **🔧 Correcciones Implementadas:**

1. **Modelos SQLAlchemy simplificados** - Sin tipos `Numeric` problemáticos
2. **Uso de `Float` en lugar de `Decimal`** - Evita errores de SQLAlchemy
3. **Estructura de archivos optimizada** - Un solo archivo principal (`app_final.py`)
4. **Scripts de inicialización corregidos** - Sin errores de importación circular

## 🚀 **Instalación y Uso**

### **Opción 1: Script Automático (Recomendado)**
```bash
# Ejecutar el script de inicio
iniciar_sistema.bat
```

### **Opción 2: Manual**
```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Inicializar base de datos
python init_final.py

# 3. Ejecutar sistema
python app_final.py

# 4. Abrir navegador en: http://localhost:5000
```

## 📋 **Regímenes Laborales Soportados**

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
- **Préstamos y Adelantos**: Descuentos automáticos

### **Para Locadores**
- **Retención 4ta Categoría**: 8% (si monto > S/. 1,500 y no está suspendido)

## 🛠️ **Tecnologías Utilizadas**

- **Backend**: Python 3.x + Flask
- **Base de Datos**: SQLite 3
- **Frontend**: HTML5 + Bootstrap 5 + JavaScript
- **Iconos**: Font Awesome 6

## 📁 **Estructura del Proyecto Final**

```
SisPla_Phyton/
├── app_final.py           # Aplicación principal (TODO EN UNO)
├── init_final.py          # Script de inicialización corregido
├── test_final.py          # Pruebas del sistema
├── iniciar_sistema.bat    # Script de inicio automático
├── requirements.txt       # Dependencias del proyecto
├── templates/            # Plantillas HTML
│   ├── base.html
│   ├── index.html
│   ├── empresas.html
│   ├── nueva_empresa.html
│   ├── personal.html
│   ├── nuevo_empleado.html
│   ├── nuevo_locador.html
│   └── planilla.html
├── static/               # Archivos estáticos
└── sispla.db            # Base de datos SQLite (se crea automáticamente)
```

## 🎯 **Funcionalidades Principales**

### **✅ Gestión de Empresas**
- Crear hasta 5 empresas simultáneamente
- Configurar régimen laboral por empresa
- Gestión de información empresarial

### **✅ Gestión de Personal**
- Registro de empleados con sueldo fijo
- Registro de locadores de servicios
- Configuración de pensiones (ONP/AFP)
- Control de estado activo/inactivo

### **✅ Cálculo de Planillas**
- Cálculo automático según régimen laboral
- Beneficios sociales diferenciados
- Descuentos por pensión e impuestos
- Pagos quincenales y mensuales
- Exportación de resultados

### **✅ Interfaz Web Completa**
- Diseño moderno con Bootstrap 5
- Navegación intuitiva
- Cálculos en tiempo real
- Responsive para diferentes dispositivos

## 🧪 **Pruebas del Sistema**

El sistema incluye pruebas automáticas que verifican:

1. **Inicialización de base de datos**
2. **Creación de empresas y personal**
3. **Cálculo de planillas por régimen**
4. **Aplicación de beneficios sociales**
5. **Cálculo de descuentos**

## 🚨 **Consideraciones Importantes**

### **Limitaciones del Sistema**
- Diseñado para uso interno (intranet)
- Máximo 5 empresas simultáneas
- Cálculos basados en legislación peruana vigente
- Requiere actualización manual de tasas y umbrales

### **Mantenimiento**
- Respaldar regularmente la base de datos `sispla.db`
- Actualizar tasas de pensión según cambios normativos
- Revisar umbrales de impuestos anualmente

## 📞 **Soporte**

Para consultas técnicas o reportar problemas:
- Revisar la documentación del código
- Verificar la configuración de la base de datos
- Consultar los logs de la aplicación

## 📄 **Licencia**

Sistema desarrollado para uso interno empresarial. Cumple con la legislación laboral peruana vigente.

---

## 🎉 **¡SISTEMA COMPLETAMENTE FUNCIONAL!**

El sistema está **listo para usar** y resuelve completamente el error de SQLAlchemy. Puedes:

1. **Ejecutar** `iniciar_sistema.bat`
2. **Abrir** http://localhost:5000 en tu navegador
3. **Crear** empresas con diferentes regímenes laborales
4. **Registrar** empleados y locadores
5. **Calcular** planillas mensuales automáticamente

**Desarrollado con ❤️ para el sector empresarial peruano**
