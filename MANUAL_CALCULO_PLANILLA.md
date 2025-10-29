# Manual de Funcionamiento - Cálculo de Planilla

## 📋 **Sistema de Planillas Multirégimen Perú**

### **🎯 Objetivo del Sistema**
El sistema calcula automáticamente las planillas de empleados y locadores según el régimen laboral de la empresa, aplicando las reglas establecidas por la legislación peruana.

---

## 🏢 **Regímenes Laborales Soportados**

### **1. Microempresa (REMYPE)**
- **Vacaciones**: 15 días anuales
- **CTS**: NO corresponde
- **Gratificaciones**: NO corresponde
- **Asignación Familiar**: NO corresponde

### **2. Pequeña Empresa (REMYPE)**
- **Vacaciones**: 15 días anuales
- **CTS**: 15 días por año de servicio
- **Gratificaciones**: Medio sueldo en Julio y Diciembre
- **Asignación Familiar**: S/. 102.50 (si sueldo ≤ S/. 1025)

### **3. Régimen General**
- **Vacaciones**: 30 días anuales
- **CTS**: Un sueldo anual
- **Gratificaciones**: Sueldo + 9% en Julio y Diciembre
- **Asignación Familiar**: S/. 102.50 (si sueldo ≤ S/. 1025)

---

## 💰 **Cálculo de Planilla - Proceso Detallado**

### **Paso 1: Cálculo de Días Trabajados**
```
Días Trabajados = 30 - Días Faltados
Días Faltados = Faltas Injustificadas + (Permisos Injustificados × 0.5)
```

### **Paso 2: Ajuste de Sueldo Base**
```
Sueldo Ajustado = Sueldo Base × (Días Trabajados / 30)
```

### **Paso 3: Aplicación de Tipo de Pago**
```
Si Tipo de Pago = "Quincenal":
    Sueldo Ajustado = Sueldo Ajustado × 0.5 (50%)

Si Tipo de Pago = "Mensual":
    Sueldo Ajustado = Sueldo Ajustado × 1.0 (100%)
```

### **Paso 4: Cálculo de Beneficios Sociales**

#### **Vacaciones**
```
Microempresa/Pequeña Empresa:
    Vacaciones = Sueldo Ajustado × (15 / 360)

Régimen General:
    Vacaciones = Sueldo Ajustado × (30 / 360)
```

#### **CTS (Compensación por Tiempo de Servicios)**
```
Microempresa:
    CTS = 0

Pequeña Empresa:
    CTS = Sueldo Ajustado × (15 / 12)

Régimen General:
    CTS = Sueldo Ajustado
```

#### **Gratificaciones**
```
Microempresa:
    Gratificación = 0

Pequeña Empresa (Julio y Diciembre):
    Gratificación = Sueldo Ajustado / 2

Régimen General (Julio y Diciembre):
    Gratificación = Sueldo Ajustado × 1.09
```

#### **Asignación Familiar**
```
Si Sueldo Ajustado ≤ S/. 1025:
    Asignación Familiar = S/. 102.50
Si Sueldo Ajustado > S/. 1025:
    Asignación Familiar = 0
```

### **Paso 5: Cálculo de Descuentos**

#### **Pensión**
```
ONP: Pensión = Sueldo Ajustado × 0.13 (13%)
AFP: Pensión = Sueldo Ajustado × 0.12 (12%)
```

#### **Impuesto a la Renta (5ta Categoría)**
```
Si Sueldo Ajustado > S/. 1025:
    Impuesto Renta = (Sueldo Ajustado - 1025) × 0.08
Si Sueldo Ajustado ≤ S/. 1025:
    Impuesto Renta = 0
```

#### **Préstamos**
```
Descuento Préstamos = Suma de Cuotas Mensuales Activas
```

#### **Adelantos**
```
Descuento Adelantos = Suma de Adelantos Pendientes para el Mes
```

### **Paso 6: Cálculo Final**
```
Total Ingresos = Sueldo Ajustado + Vacaciones + CTS + Gratificación + Asignación Familiar
Total Descuentos = Pensión + Impuesto Renta + Préstamos + Adelantos
Neto a Pagar = Total Ingresos - Total Descuentos
```

---

## 📅 **Control de Ausencias**

### **Tipos de Ausencias**
- **Falta**: 1 día completo (8 horas)
- **Permiso**: 0.5 días (4 horas)
- **Vacaciones**: 1 día completo (8 horas)
- **Licencia**: 1 día completo (8 horas)

### **Impacto en el Cálculo**
- **Ausencias Justificadas**: NO afectan el sueldo
- **Ausencias Injustificadas**: Descuentan proporcionalmente del sueldo

---

## 💳 **Gestión de Deudas Internas**

### **Préstamos**
- **Cuota Mensual**: Se descuenta automáticamente cada mes
- **Estado**: Activo hasta completar el pago total
- **Cálculo**: Monto Total ÷ Número de Cuotas

### **Adelantos**
- **Descuento**: Se aplica en el mes específico programado
- **Estado**: Pendiente hasta ser aplicado
- **Uso**: Adelantos de sueldo para necesidades específicas

---

## 🏦 **Información Bancaria**

### **Campos Disponibles**
- **Banco**: Selección de banco principal
- **Número de Cuenta**: Cuenta bancaria para transferencias
- **Tipo de Pago**: Mensual o Quincenal

### **Bancos Soportados**
- Banco de Crédito del Perú (BCP)
- BBVA Continental
- Scotiabank
- Interbank
- BanBif
- Banco Pichincha
- Otro

---

## 📊 **Ejemplo de Cálculo**

### **Empleado del Régimen General**
- **Sueldo Base**: S/. 1,500
- **Días Trabajados**: 28 (2 faltas injustificadas)
- **Tipo de Pago**: Mensual
- **Mes**: Julio (Gratificaciones)

#### **Cálculo Paso a Paso:**

1. **Sueldo Ajustado**: 1,500 × (28/30) = S/. 1,400
2. **Vacaciones**: 1,400 × (30/360) = S/. 116.67
3. **CTS**: S/. 1,400
4. **Gratificación**: 1,400 × 1.09 = S/. 1,526
5. **Asignación Familiar**: S/. 102.50
6. **Pensión ONP**: 1,400 × 0.13 = S/. 182
7. **Impuesto Renta**: (1,400 - 1,025) × 0.08 = S/. 30

#### **Totales:**
- **Total Ingresos**: 1,400 + 116.67 + 1,400 + 1,526 + 102.50 = S/. 4,545.17
- **Total Descuentos**: 182 + 30 = S/. 212
- **Neto a Pagar**: 4,545.17 - 212 = S/. 4,333.17

---

## 🔧 **Configuración del Sistema**

### **Parámetros Configurables**
- **Umbral de Asignación Familiar**: S/. 1025
- **Tasa de Pensión ONP**: 13%
- **Tasa de Pensión AFP**: 12%
- **Tasa de Impuesto Renta**: 8%
- **Umbral de Retención 4ta Categoría**: S/. 1,500

### **Meses Especiales**
- **Julio**: Gratificaciones (Pequeña Empresa y General)
- **Diciembre**: Gratificaciones (Pequeña Empresa y General)

---

## 📋 **Reportes Disponibles**

### **Planilla de Empleados**
- Detalle por empleado con todos los cálculos
- Información bancaria para transferencias
- Tipo de pago aplicado
- Resumen de beneficios y descuentos

### **Planilla de Locadores**
- Monto mensual acordado
- Retención 4ta Categoría (si aplica)
- Estado de suspensión
- Información bancaria

### **Totales Generales**
- Total de empleados procesados
- Total de locadores procesados
- Suma total de ingresos
- Suma total de descuentos
- Neto total a pagar

---

## ⚠️ **Consideraciones Importantes**

### **Validaciones del Sistema**
- Los empleados deben estar activos para ser procesados
- Los locadores suspendidos no generan retención 4ta Categoría
- Las ausencias se calculan por mes específico
- Los adelantos se aplican solo en el mes programado

### **Cumplimiento Legal**
- El sistema cumple con la legislación laboral peruana vigente
- Los cálculos están basados en las normas del Ministerio de Trabajo
- Se recomienda revisar actualizaciones normativas periódicamente

---

## 🆘 **Soporte y Mantenimiento**

### **Actualizaciones**
- Revisar cambios en tasas de pensión
- Verificar actualizaciones en umbrales de impuestos
- Mantener actualizada la información bancaria

### **Respaldo de Datos**
- Realizar respaldos regulares de la base de datos
- Exportar planillas calculadas para archivo
- Mantener historial de cálculos por empresa

---

**Desarrollado con ❤️ para el sector empresarial peruano**
