# 🚀 GUÍA COMPLETA PARA PRODUCCIÓN - SISTEMA DE PLANILLAS

## 📋 **PREREQUISITOS DEL SISTEMA**

### **Sistema Operativo**
- ✅ **Windows 10/11** (Recomendado)
- ✅ **Windows Server 2019/2022**
- ✅ **Ubuntu 20.04 LTS o superior**
- ✅ **CentOS 8+ o RHEL 8+**

### **Requisitos Mínimos de Hardware**
- **RAM**: 4 GB mínimo, 8 GB recomendado
- **Almacenamiento**: 2 GB libres
- **Procesador**: 2 núcleos mínimo
- **Red**: Conexión estable para acceso local

---

## 🛠️ **SOFTWARE REQUERIDO**

### **1. Python 3.8 o Superior**
```bash
# Verificar versión actual
python --version

# Si no está instalado, descargar desde:
# https://www.python.org/downloads/
```

### **2. Git (Opcional pero recomendado)**
```bash
# Para clonar el repositorio
# https://git-scm.com/downloads
```

---

## 📦 **ARCHIVOS NECESARIOS PARA PRODUCCIÓN**

### **Archivos Principales**
- ✅ `app_completo.py` - Aplicación principal
- ✅ `requirements.txt` - Dependencias
- ✅ `sistema_final_funcional.py` - Inicializador
- ✅ `templates/` - Plantillas HTML
- ✅ `static/` - Archivos CSS/JS

### **Archivos de Configuración**
- ✅ `instalar_produccion.bat` - Instalador Windows
- ✅ `instalar_produccion_linux.sh` - Instalador Linux
- ✅ `iniciar_sistema.bat` - Iniciador Windows
- ✅ `iniciar_sistema.sh` - Iniciador Linux

---

## 🚀 **PASOS DE INSTALACIÓN**

### **MÉTODO 1: INSTALACIÓN AUTOMÁTICA (RECOMENDADO)**

#### **En Windows:**
1. **Ejecutar como Administrador:**
   ```cmd
   # Hacer clic derecho en "instalar_produccion.bat"
   # Seleccionar "Ejecutar como administrador"
   ```

2. **Seguir las instrucciones en pantalla**

3. **Al finalizar, el sistema estará en:**
   ```
   C:\SisPla_Produccion\
   ```

#### **En Linux:**
1. **Dar permisos de ejecución:**
   ```bash
   chmod +x instalar_produccion_linux.sh
   ```

2. **Ejecutar instalador:**
   ```bash
   sudo ./instalar_produccion_linux.sh
   ```

3. **Al finalizar, el sistema estará en:**
   ```
   /opt/sispla_produccion/
   ```

### **MÉTODO 2: INSTALACIÓN MANUAL**

#### **Paso 1: Preparar Directorio**
```bash
# Windows
mkdir C:\SisPla_Produccion
cd C:\SisPla_Produccion

# Linux
sudo mkdir -p /opt/sispla_produccion
sudo chown $USER:$USER /opt/sispla_produccion
cd /opt/sispla_produccion
```

#### **Paso 2: Copiar Archivos**
```bash
# Copiar todos los archivos del proyecto
# Asegúrese de incluir:
# - app_completo.py
# - requirements.txt
# - sistema_final_funcional.py
# - templates/
# - static/
```

#### **Paso 3: Crear Entorno Virtual**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux
python3 -m venv venv
source venv/bin/activate
```

#### **Paso 4: Instalar Dependencias**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### **Paso 5: Inicializar Base de Datos**
```bash
python sistema_final_funcional.py
```

---

## 🎯 **CONFIGURACIÓN DE PRODUCCIÓN**

### **1. Configuración de Red**
```python
# En app_completo.py, línea 15
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
    # Para acceso local: host='127.0.0.1'
    # Para acceso de red: host='0.0.0.0'
```

### **2. Configuración de Base de Datos**
```python
# La base de datos se crea automáticamente en:
# Windows: instance/database.db
# Linux: instance/database.db
```

### **3. Configuración de Archivos**
```python
# Directorio de uploads para Excel:
UPLOAD_FOLDER = 'uploads'
# Se crea automáticamente si no existe
```

---

## 🔧 **INICIAR EL SISTEMA**

### **Método 1: Script Automático**
```bash
# Windows
C:\SisPla_Produccion\iniciar_sistema.bat

# Linux
sudo /opt/sispla_produccion/iniciar_sistema.sh
```

### **Método 2: Manual**
```bash
# Activar entorno virtual
# Windows
venv\Scripts\activate

# Linux
source venv/bin/activate

# Iniciar aplicación
python app_completo.py
```

---

## 🌐 **ACCESO AL SISTEMA**

### **URLs de Acceso**
- **Local**: http://localhost:5000
- **Red Local**: http://[IP_DEL_SERVIDOR]:5000
- **Ejemplo**: http://192.168.1.100:5000

### **Verificar IP del Servidor**
```bash
# Windows
ipconfig

# Linux
ip addr show
# o
ifconfig
```

---

## 🔒 **CONFIGURACIÓN DE SEGURIDAD**

### **1. Firewall (Windows)**
```cmd
# Permitir puerto 5000
netsh advfirewall firewall add rule name="SisPla" dir=in action=allow protocol=TCP localport=5000
```

### **2. Firewall (Linux)**
```bash
# Ubuntu/Debian
sudo ufw allow 5000

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

### **3. Usuario de Servicio (Linux)**
```bash
# Crear usuario específico
sudo useradd -r -s /bin/false sispla
sudo chown -R sispla:sispla /opt/sispla_produccion
```

---

## 📊 **MONITOREO Y MANTENIMIENTO**

### **1. Logs del Sistema**
```bash
# Los logs aparecen en la consola donde se ejecuta
# Para guardar logs en archivo:
python app_completo.py > sispla.log 2>&1
```

### **2. Backup de Base de Datos**
```bash
# Windows
copy instance\database.db backup\database_%date%.db

# Linux
cp instance/database.db backup/database_$(date +%Y%m%d).db
```

### **3. Actualización del Sistema**
```bash
# 1. Hacer backup de la base de datos
# 2. Detener el sistema (Ctrl+C)
# 3. Copiar nuevos archivos
# 4. Reiniciar el sistema
```

---

## 🚨 **SOLUCIÓN DE PROBLEMAS**

### **Error: Puerto 5000 en uso**
```bash
# Cambiar puerto en app_completo.py línea 15:
app.run(host='0.0.0.0', port=8080, debug=False)
```

### **Error: Permisos de archivo**
```bash
# Linux
sudo chmod -R 755 /opt/sispla_produccion
sudo chown -R $USER:$USER /opt/sispla_produccion
```

### **Error: Base de datos corrupta**
```bash
# Eliminar y recrear
rm instance/database.db
python sistema_final_funcional.py
```

### **Error: Módulos no encontrados**
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

---

## 📋 **CHECKLIST DE PRODUCCIÓN**

### **Pre-Instalación**
- [ ] Python 3.8+ instalado
- [ ] 4 GB RAM disponibles
- [ ] 2 GB espacio libre
- [ ] Acceso de red configurado

### **Instalación**
- [ ] Archivos copiados correctamente
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas
- [ ] Base de datos inicializada

### **Configuración**
- [ ] Firewall configurado
- [ ] Puerto 5000 abierto
- [ ] Usuario de servicio creado (Linux)
- [ ] Permisos de archivo correctos

### **Pruebas**
- [ ] Sistema inicia correctamente
- [ ] Acceso local funciona
- [ ] Acceso de red funciona
- [ ] Todas las funcionalidades operativas

---

## 🎉 **¡SISTEMA LISTO PARA PRODUCCIÓN!**

Una vez completados todos los pasos, tu sistema de planillas estará funcionando en producción y podrás:

- ✅ Gestionar hasta 5 empresas
- ✅ Calcular planillas quincenales y mensuales
- ✅ Exportar a Excel
- ✅ Cargar personal masivamente
- ✅ Gestionar ausencias y deudas
- ✅ Acceder desde cualquier navegador en la red local

**¡El sistema está listo para usar en producción!** 🚀
