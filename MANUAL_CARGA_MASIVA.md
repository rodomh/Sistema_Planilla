# Manual de Carga Masiva de Personal y Locadores

## 📋 Índice
1. [Introducción](#introducción)
2. [Formato del Archivo Excel](#formato-del-archivo-excel)
3. [Estructura de la Hoja "Empleados"](#estructura-de-la-hoja-empleados)
4. [Estructura de la Hoja "Locadores"](#estructura-de-la-hoja-locadores)
5. [Ejemplos de Datos](#ejemplos-de-datos)
6. [Validaciones y Reglas](#validaciones-y-reglas)
7. [Proceso de Carga](#proceso-de-carga)
8. [Solución de Problemas](#solución-de-problemas)

---

## 🎯 Introducción

El sistema de planillas multirégimen permite la carga masiva de personal (empleados y locadores) mediante archivos Excel. Este manual describe la estructura exacta que deben tener estos archivos para una carga exitosa.

### Requisitos del Archivo
- **Formato**: Excel (.xlsx)
- **Tamaño máximo**: 16MB
- **Hojas requeridas**: "Empleados" y/o "Locadores"
- **Codificación**: UTF-8

---

## 📊 Formato del Archivo Excel

El archivo Excel debe contener **exactamente** las siguientes hojas:

### Hojas Disponibles
1. **"Empleados"** - Para cargar empleados de la empresa
2. **"Locadores"** - Para cargar locadores de servicios

### Estructura General
- **Fila 1**: Encabezados (obligatorio)
- **Fila 2 en adelante**: Datos de personal
- **No dejar filas vacías** entre los datos

---

## 👥 Estructura de la Hoja "Empleados"

### Encabezados Obligatorios (Fila 1)

| Columna | Campo | Tipo | Obligatorio | Descripción |
|---------|-------|------|-------------|-------------|
| A | Nombres | Texto | ✅ | Nombre(s) del empleado |
| B | Apellidos | Texto | ✅ | Apellidos del empleado |
| C | DNI | Texto | ✅ | Número de DNI (8 dígitos) |
| D | Sueldo Base | Número | ✅ | Sueldo mensual en soles |
| E | Fecha Ingreso | Fecha | ✅ | Fecha de ingreso (YYYY-MM-DD) |
| F | Tipo Pensión | Texto | ✅ | "ONP" o "AFP" |
| G | AFP Código | Texto | ❌ | Código AFP (solo si Tipo Pensión = "AFP") |
| H | Cuenta Bancaria | Texto | ❌ | Número de cuenta bancaria |
| I | Banco | Texto | ❌ | Nombre del banco |
| J | Tipo Pago | Texto | ❌ | "mensual" o "quincenal" |

### Ejemplo de Datos para Empleados

| Nombres | Apellidos | DNI | Sueldo Base | Fecha Ingreso | Tipo Pensión | AFP Código | Cuenta Bancaria | Banco | Tipo Pago |
|---------|-----------|-----|-------------|---------------|--------------|------------|-----------------|-------|-----------|
| Juan | Pérez García | 12345678 | 1500.00 | 2024-01-15 | ONP | | 1234567890123456 | BCP | mensual |
| María | López Silva | 87654321 | 2000.00 | 2024-02-01 | AFP | PRIMA | 9876543210987654 | BBVA | quincenal |
| Carlos | Mendoza Vega | 11223344 | 1800.00 | 2024-03-10 | ONP | | 1122334455667788 | SCOTIABANK | mensual |

---

## 💼 Estructura de la Hoja "Locadores"

### Encabezados Obligatorios (Fila 1)

| Columna | Campo | Tipo | Obligatorio | Descripción |
|---------|-------|------|-------------|-------------|
| A | Nombres | Texto | ✅ | Nombre(s) del locador |
| B | Apellidos | Texto | ✅ | Apellidos del locador |
| C | DNI | Texto | ✅ | Número de DNI (8 dígitos) |
| D | Monto Mensual | Número | ✅ | Monto mensual en soles |
| E | Fecha Inicio | Fecha | ✅ | Fecha de inicio (YYYY-MM-DD) |
| F | Suspendido | Lógico | ❌ | TRUE o FALSE |
| G | Cuenta Bancaria | Texto | ❌ | Número de cuenta bancaria |
| H | Banco | Texto | ❌ | Nombre del banco |

### Ejemplo de Datos para Locadores

| Nombres | Apellidos | DNI | Monto Mensual | Fecha Inicio | Suspendido | Cuenta Bancaria | Banco |
|---------|-----------|-----|---------------|--------------|------------|-----------------|-------|
| Ana | Rodríguez Castro | 55667788 | 2500.00 | 2024-01-20 | FALSE | 5566778899001122 | BCP |
| Luis | Herrera Morales | 99887766 | 3000.00 | 2024-02-15 | FALSE | 9988776655443322 | BBVA |
| Elena | Díaz Paz | 44332211 | 2800.00 | 2024-03-05 | TRUE | 4433221100998877 | SCOTIABANK |

---

## 📝 Ejemplos de Datos

### Plantilla Completa de Empleados

```
Nombres          | Apellidos        | DNI      | Sueldo Base | Fecha Ingreso | Tipo Pensión | AFP Código | Cuenta Bancaria    | Banco      | Tipo Pago
Juan Carlos      | Pérez García     | 12345678 | 1500.00     | 2024-01-15    | ONP          |            | 1234567890123456   | BCP        | mensual
María Elena      | López Silva      | 87654321 | 2000.00     | 2024-02-01    | AFP          | PRIMA      | 9876543210987654   | BBVA       | quincenal
Carlos Alberto   | Mendoza Vega      | 11223344 | 1800.00     | 2024-03-10    | ONP          |            | 1122334455667788   | SCOTIABANK | mensual
Ana Patricia     | Torres Díaz      | 55667788 | 2200.00     | 2024-04-05    | AFP          | HABITAT    | 5566778899001122   | INTERBANK  | mensual
```

### Plantilla Completa de Locadores

```
Nombres          | Apellidos        | DNI      | Monto Mensual | Fecha Inicio | Suspendido | Cuenta Bancaria    | Banco
Ana María        | Rodríguez Castro | 55667788 | 2500.00       | 2024-01-20   | FALSE      | 5566778899001122   | BCP
Luis Fernando    | Herrera Morales  | 99887766 | 3000.00       | 2024-02-15   | FALSE      | 9988776655443322   | BBVA
Elena Beatriz    | Díaz Paz         | 44332211 | 2800.00       | 2024-03-05   | TRUE       | 4433221100998877   | SCOTIABANK
Roberto Carlos   | Vega López       | 77889900 | 3200.00       | 2024-04-10   | FALSE      | 7788990011223344   | BANBIF
```

---

## ✅ Validaciones y Reglas

### Campos Obligatorios
- **Nombres**: No puede estar vacío
- **Apellidos**: No puede estar vacío
- **DNI**: Debe tener exactamente 8 dígitos
- **Sueldo Base/Monto Mensual**: Debe ser un número positivo
- **Fecha Ingreso/Fecha Inicio**: Debe estar en formato YYYY-MM-DD

### Validaciones Específicas

#### Para Empleados
- **Tipo Pensión**: Solo acepta "ONP" o "AFP"
- **AFP Código**: Requerido solo si Tipo Pensión = "AFP"
- **Tipo Pago**: Solo acepta "mensual" o "quincenal"
- **Sueldo Base**: Debe ser mayor a 0

#### Para Locadores
- **Suspendido**: Solo acepta TRUE o FALSE
- **Monto Mensual**: Debe ser mayor a 0

### Formatos de Fecha
- **Formato requerido**: YYYY-MM-DD
- **Ejemplos válidos**: 2024-01-15, 2024-12-31
- **Ejemplos inválidos**: 15/01/2024, 2024-1-15

### Bancos Soportados
- Banco de Crédito del Perú (BCP)
- BBVA Continental
- Scotiabank
- Interbank
- BanBif
- Banco Pichincha
- Otro

---

## 🔄 Proceso de Carga

### Paso 1: Preparar el Archivo
1. Descargar la plantilla desde el sistema
2. Completar los datos siguiendo el formato especificado
3. Guardar como archivo Excel (.xlsx)

### Paso 2: Cargar al Sistema
1. Acceder a la empresa correspondiente
2. Ir a "Ver Personal"
3. Hacer clic en "Cargar desde Excel"
4. Seleccionar el archivo preparado
5. Hacer clic en "Cargar Datos"

### Paso 3: Verificar Resultados
1. El sistema mostrará el número de registros cargados
2. Verificar en la lista de personal que los datos se cargaron correctamente
3. Revisar que no haya errores en los datos

---

## ⚠️ Solución de Problemas

### Errores Comunes

#### Error: "No se seleccionó ningún archivo"
- **Causa**: No se seleccionó un archivo antes de hacer clic en "Cargar Datos"
- **Solución**: Seleccionar un archivo Excel (.xlsx) válido

#### Error: "El archivo debe ser un Excel (.xlsx)"
- **Causa**: El archivo no es un Excel o tiene extensión incorrecta
- **Solución**: Guardar el archivo como .xlsx

#### Error: "Error al procesar el archivo"
- **Causa**: El archivo tiene formato incorrecto o datos inválidos
- **Solución**: 
  - Verificar que los encabezados estén correctos
  - Revisar que no haya filas vacías entre los datos
  - Validar formatos de fecha y números

#### Error: "DNI debe tener 8 dígitos"
- **Causa**: El DNI no tiene exactamente 8 dígitos
- **Solución**: Corregir el DNI para que tenga 8 dígitos

#### Error: "Tipo Pensión debe ser ONP o AFP"
- **Causa**: Valor incorrecto en la columna Tipo Pensión
- **Solución**: Cambiar a "ONP" o "AFP"

### Verificaciones Previas

Antes de cargar, verificar:
- [ ] El archivo es .xlsx
- [ ] Los encabezados están en la fila 1
- [ ] No hay filas vacías entre los datos
- [ ] Los DNIs tienen 8 dígitos
- [ ] Las fechas están en formato YYYY-MM-DD
- [ ] Los números no tienen formato de texto
- [ ] Los valores de Tipo Pensión son "ONP" o "AFP"

---

## 📞 Soporte

Si encuentras problemas durante la carga masiva:

1. **Verificar el formato** del archivo según este manual
2. **Revisar los datos** para asegurar que cumplan las validaciones
3. **Probar con pocos registros** primero para identificar el problema
4. **Contactar al administrador** del sistema si el problema persiste

---

## 📋 Checklist de Carga Masiva

### Antes de Cargar
- [ ] Archivo guardado como .xlsx
- [ ] Encabezados correctos en fila 1
- [ ] Datos completos en campos obligatorios
- [ ] Formatos de fecha correctos (YYYY-MM-DD)
- [ ] DNIs con 8 dígitos
- [ ] Valores válidos en campos de selección
- [ ] Sin filas vacías entre datos

### Después de Cargar
- [ ] Verificar número de registros cargados
- [ ] Revisar datos en la lista de personal
- [ ] Confirmar que no hay errores
- [ ] Probar funcionalidades del sistema

---

**¡Con este manual podrás realizar cargas masivas exitosas de personal y locadores en el sistema de planillas multirégimen!** 🚀
