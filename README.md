# Sistema de Planillas Multirégimen Perú 🇵🇪

Sistema funcional y standalone para gestión de planillas en Perú, capaz de manejar hasta 5 empresas simultáneamente con diferentes regímenes laborales: Microempresa (REMYPE), Pequeña Empresa (REMYPE) y Régimen General.

## 🚀 Características Principales

- **Multirégimen**: Gestión simultánea de hasta 5 empresas con diferentes regímenes laborales
- **Cálculo Automático**: Beneficios sociales diferenciados según régimen laboral
- **Standalone**: Funciona sin conexión a internet usando SQLite
- **Intranet**: Diseñado para uso interno en empresas
- **Completo**: Gestión de personal, ausencias, deudas internas y cálculos de planilla

## 📋 Regímenes Laborales Soportados

### Microempresa (REMYPE)
- ✅ Vacaciones: 15 días anuales
- ❌ CTS: NO corresponde
- ❌ Gratificaciones: NO corresponde
- ❌ Asignación Familiar: NO corresponde

### Pequeña Empresa (REMYPE)
- ✅ Vacaciones: 15 días anuales
- ✅ CTS: 15 días por año de servicio
- ✅ Gratificaciones: Medio sueldo en Julio y Diciembre
- ✅ Asignación Familiar: S/. 102.50 (si sueldo ≤ S/. 1025)

### Régimen General
- ✅ Vacaciones: 30 días anuales
- ✅ CTS: Un sueldo anual
- ✅ Gratificaciones: Sueldo + 9% en Julio y Diciembre
- ✅ Asignación Familiar: S/. 102.50 (si sueldo ≤ S/. 1025)

## 💰 Descuentos Aplicables

### Para Empleados
- **Pensión ONP**: 13% del sueldo
- **Pensión AFP**: 12% del sueldo (según AFP)
- **Impuesto a la Renta 5ta Categoría**: Según tramos establecidos
- **Préstamos y Adelantos**: Descuentos automáticos

### Para Locadores
- **Retención 4ta Categoría**: 8% (si monto > S/. 1,500 y no está suspendido)

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3.x + Flask
- **Base de Datos**: SQLite 3
- **Frontend**: HTML5 + Bootstrap 5 + JavaScript
- **Iconos**: Font Awesome 6

## 📦 Instalación

### Requisitos Previos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
```bash
# Si tienes git instalado
git clone <url-del-repositorio>
cd SisPla_Phyton

# O simplemente descargar y extraer el archivo ZIP
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Inicializar la base de datos**
```bash
python init_db_simple.py
```

4. **Ejecutar el sistema**
```bash
python app_simple.py
```

5. **Abrir en el navegador**
```
http://localhost:5000
```

## 🎯 Uso del Sistema

### 1. Configuración Inicial
- Crear empresas con su régimen laboral correspondiente
- Registrar empleados con su información personal y laboral
- Registrar locadores de servicios si aplica

### 2. Gestión Diaria
- Registrar ausencias, permisos y faltas
- Gestionar préstamos y adelantos
- Controlar días trabajados

### 3. Cálculo de Planillas
- Seleccionar empresa y período
- Calcular planilla mensual o quincenal
- Revisar beneficios y descuentos aplicados
- Exportar resultados

## 📁 Estructura del Proyecto

```
SisPla_Phyton/
├── app.py                 # Aplicación principal Flask
├── models.py              # Modelos de base de datos
├── calculadora_planilla.py # Lógica de cálculo de planillas
├── gestion_personal.py    # Gestión de personal y ausencias
├── gestion_deudas.py      # Gestión de préstamos y adelantos
├── init_db.py            # Script de inicialización
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
├── static/               # Archivos estáticos (CSS, JS, imágenes)
└── sispla.db            # Base de datos SQLite (se crea automáticamente)
```

## 🔧 Configuración Avanzada

### Modificar Umbrales y Tasas
El sistema permite modificar los siguientes valores desde la base de datos:

- Umbral mínimo no afecto para impuesto a la renta
- Umbral para retención 4ta categoría
- Tasas de pensión por AFP
- Monto de asignación familiar

### Personalización por Empresa
Cada empresa puede tener:
- Diferente régimen laboral
- Configuraciones específicas
- Personal independiente
- Cálculos diferenciados

## 📊 Funcionalidades Principales

### Gestión de Empresas
- ✅ Crear hasta 5 empresas simultáneamente
- ✅ Configurar régimen laboral por empresa
- ✅ Gestión de información empresarial

### Gestión de Personal
- ✅ Registro de empleados con sueldo fijo
- ✅ Registro de locadores de servicios
- ✅ Configuración de pensiones (ONP/AFP)
- ✅ Control de estado activo/inactivo

### Control de Ausencias
- ✅ Registro de faltas, permisos y vacaciones
- ✅ Justificación de ausencias
- ✅ Cálculo automático de días trabajados
- ✅ Estadísticas por empresa y empleado

### Deudas Internas
- ✅ Gestión de préstamos con cuotas mensuales
- ✅ Adelantos de sueldo
- ✅ Descuentos automáticos en planilla
- ✅ Control de capacidad de pago

### Cálculo de Planillas
- ✅ Cálculo automático según régimen laboral
- ✅ Beneficios sociales diferenciados
- ✅ Descuentos por pensión e impuestos
- ✅ Pagos quincenales y mensuales
- ✅ Exportación de resultados

## 🚨 Consideraciones Importantes

### Limitaciones del Sistema
- Diseñado para uso interno (intranet)
- Máximo 5 empresas simultáneas
- Cálculos basados en legislación peruana vigente
- Requiere actualización manual de tasas y umbrales

### Mantenimiento
- Respaldar regularmente la base de datos `sispla.db`
- Actualizar tasas de pensión según cambios normativos
- Revisar umbrales de impuestos anualmente

## 📞 Soporte

Para consultas técnicas o reportar problemas:
- Revisar la documentación del código
- Verificar la configuración de la base de datos
- Consultar los logs de la aplicación

## 📄 Licencia

Sistema desarrollado para uso interno empresarial. Cumple con la legislación laboral peruana vigente.

---

**Desarrollado con ❤️ para el sector empresarial peruano**

