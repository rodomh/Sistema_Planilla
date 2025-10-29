# 📋 Plan de Pruebas de Funcionalidad - Sistema de Planillas Multirégimen

## 🎯 Objetivo
Verificar que todas las funcionalidades del sistema de planillas multirégimen funcionen correctamente según los requisitos establecidos.

---

## 📊 Funcionalidades a Probar

### 1. **Gestión de Empresas** ✅
- [ ] **Crear empresa** con diferentes regímenes laborales
  - [ ] Microempresa (REMYPE)
  - [ ] Pequeña Empresa (REMYPE) 
  - [ ] Régimen General
- [ ] **Listar empresas** con conteo correcto de personal
- [ ] **Validar campos obligatorios** (nombre, RUC, régimen)

### 2. **Gestión de Empleados** ✅
- [ ] **Crear empleado** con todos los campos
  - [ ] Información personal (nombres, apellidos, DNI)
  - [ ] Información laboral (sueldo, fecha ingreso, tipo pensión)
  - [ ] **Tipo de pago** (mensual/quincenal)
  - [ ] **Información bancaria** (banco, cuenta)
  - [ ] **Descuento por alimentos** (solo fin de mes)
- [ ] **Editar empleado** existente
- [ ] **Eliminar empleado** (marcar como inactivo)
- [ ] **Validar DNI** (8 dígitos)
- [ ] **Validar campos obligatorios**

### 3. **Gestión de Locadores** ✅
- [ ] **Crear locador** con todos los campos
  - [ ] Información personal (nombres, apellidos, DNI)
  - [ ] Información contractual (monto mensual, fecha inicio)
  - [ ] **Información bancaria** (banco, cuenta)
  - [ ] **Descuento por alimentos** (solo fin de mes)
  - [ ] Estado (activo/suspendido)
- [ ] **Editar locador** existente
- [ ] **Eliminar locador** (marcar como inactivo)
- [ ] **Validar campos obligatorios**

### 4. **Cálculo de Planillas por Régimen** ✅

#### 4.1 **Microempresa (REMYPE)**
- [ ] **Vacaciones**: 15 días anuales
- [ ] **CTS**: NO corresponde
- [ ] **Gratificaciones**: NO corresponde
- [ ] **Asignación Familiar**: NO corresponde
- [ ] **Descuentos**: Pensión (13% ONP / 12% AFP), Impuesto Renta

#### 4.2 **Pequeña Empresa (REMYPE)**
- [ ] **Vacaciones**: 15 días anuales
- [ ] **CTS**: 15 días por año de servicio
- [ ] **Gratificaciones**: 50% en Julio y Diciembre
- [ ] **Asignación Familiar**: S/. 102.50 (si sueldo ≤ S/. 1025)
- [ ] **Descuentos**: Pensión, Impuesto Renta

#### 4.3 **Régimen General**
- [ ] **Vacaciones**: 30 días anuales
- [ ] **CTS**: Un sueldo anual
- [ ] **Gratificaciones**: Sueldo + 9% en Julio y Diciembre
- [ ] **Asignación Familiar**: S/. 102.50 (si sueldo ≤ S/. 1025)
- [ ] **Descuentos**: Pensión, Impuesto Renta

### 5. **Tipos de Pago** ✅
- [ ] **Pago Mensual**: 100% del sueldo base
- [ ] **Pago Quincenal**: 50% del sueldo base
- [ ] **Aplicación correcta** en cálculo de planilla
- [ ] **Visualización** del tipo de pago en planilla

### 6. **Descuentos Judiciales** ✅
- [ ] **Descuento por alimentos** para empleados
- [ ] **Descuento por alimentos** para locadores
- [ ] **Aplicación solo en pago mensual** (fin de mes)
- [ ] **No aplicación en pago quincenal**
- [ ] **Visualización** en planilla calculada

### 7. **Información Bancaria** ✅
- [ ] **Campos bancarios** en empleados y locadores
- [ ] **Selección de banco** de lista predefinida
- [ ] **Número de cuenta** (hasta 20 caracteres)
- [ ] **Visualización** en planilla calculada

### 8. **Exportación a Excel** ✅
- [ ] **Exportar planilla** a archivo Excel
- [ ] **Hoja de empleados** con todos los cálculos
- [ ] **Hoja de locadores** con todos los cálculos
- [ ] **Formato correcto** de archivo (.xlsx)
- [ ] **Nombre de archivo** descriptivo

### 9. **Interfaz de Usuario** ✅
- [ ] **Navegación** entre secciones
- [ ] **Formularios** responsivos y validados
- [ ] **Mensajes de confirmación** y error
- [ ] **Tablas** con información clara
- [ ] **Botones** de acción funcionales

---

## 🧪 Casos de Prueba Específicos

### **Caso 1: Empleado Quincenal con Descuento Alimentos**
1. Crear empleado con:
   - Sueldo base: S/. 2000
   - Tipo pago: Quincenal
   - Descuento alimentos: S/. 200
2. Calcular planilla para Octubre 2024
3. **Verificar**:
   - Sueldo ajustado: S/. 1000 (50%)
   - Descuento alimentos: S/. 0 (no aplica en quincenal)
   - Cálculos correctos según régimen

### **Caso 2: Empleado Mensual con Descuento Alimentos**
1. Crear empleado con:
   - Sueldo base: S/. 2000
   - Tipo pago: Mensual
   - Descuento alimentos: S/. 200
2. Calcular planilla para Octubre 2024
3. **Verificar**:
   - Sueldo ajustado: S/. 2000 (100%)
   - Descuento alimentos: S/. 200 (aplica en mensual)
   - Cálculos correctos según régimen

### **Caso 3: Locador con Descuento Alimentos**
1. Crear locador con:
   - Monto mensual: S/. 3000
   - Descuento alimentos: S/. 300
2. Calcular planilla para Octubre 2024
3. **Verificar**:
   - Retención 4ta: S/. 240 (8% de 3000)
   - Descuento alimentos: S/. 300
   - Total descuentos: S/. 540

### **Caso 4: Exportación Excel**
1. Calcular planilla con empleados y locadores
2. Exportar a Excel
3. **Verificar**:
   - Archivo se descarga correctamente
   - Contiene hojas de empleados y locadores
   - Datos son correctos y completos

---

## 🔍 Criterios de Aceptación

### **Funcionalidad Core**
- ✅ Sistema permite gestionar hasta 5 empresas
- ✅ Cada empresa tiene régimen laboral configurado
- ✅ Cálculos de planilla son correctos según régimen
- ✅ Interfaz web es funcional y responsive

### **Tipos de Pago**
- ✅ Pago quincenal aplica 50% del sueldo
- ✅ Pago mensual aplica 100% del sueldo
- ✅ Descuentos por alimentos solo en pago mensual

### **Descuentos y Beneficios**
- ✅ Beneficios se calculan según régimen laboral
- ✅ Descuentos se aplican correctamente
- ✅ Información bancaria se almacena y muestra

### **Exportación**
- ✅ Excel se genera correctamente
- ✅ Contiene toda la información de la planilla
- ✅ Formato es profesional y legible

---

## 📝 Checklist de Pruebas

### **Preparación**
- [ ] Base de datos inicializada
- [ ] Sistema ejecutándose en localhost:5000
- [ ] Navegador web abierto

### **Pruebas de Empresas**
- [ ] Crear empresa Microempresa
- [ ] Crear empresa Pequeña Empresa
- [ ] Crear empresa Régimen General
- [ ] Verificar listado de empresas

### **Pruebas de Empleados**
- [ ] Crear empleado con pago mensual
- [ ] Crear empleado con pago quincenal
- [ ] Crear empleado con descuento alimentos
- [ ] Editar empleado existente
- [ ] Eliminar empleado

### **Pruebas de Locadores**
- [ ] Crear locador con descuento alimentos
- [ ] Crear locador suspendido
- [ ] Editar locador existente
- [ ] Eliminar locador

### **Pruebas de Planilla**
- [ ] Calcular planilla Microempresa
- [ ] Calcular planilla Pequeña Empresa
- [ ] Calcular planilla Régimen General
- [ ] Verificar cálculos de pago quincenal
- [ ] Verificar descuentos por alimentos
- [ ] Exportar planilla a Excel

### **Pruebas de Validación**
- [ ] Validar DNI de 8 dígitos
- [ ] Validar campos obligatorios
- [ ] Validar formato de fechas
- [ ] Validar valores numéricos

---

## 🚀 Instrucciones de Ejecución

1. **Iniciar sistema**:
   ```bash
   python app_completo.py
   ```

2. **Abrir navegador** en `http://localhost:5000`

3. **Ejecutar pruebas** siguiendo el checklist

4. **Documentar resultados** de cada prueba

5. **Reportar errores** encontrados

---

## 📊 Métricas de Éxito

- **100%** de funcionalidades core implementadas
- **0** errores críticos en cálculos de planilla
- **100%** de validaciones funcionando
- **Excel** se exporta correctamente
- **Interfaz** es responsive y funcional

---

**¡Con este plan de pruebas podrás verificar que todas las funcionalidades del sistema funcionen correctamente!** 🎯
