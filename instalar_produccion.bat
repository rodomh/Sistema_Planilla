@echo off
echo ========================================
echo INSTALACION DEL SISTEMA DE PLANILLAS
echo ========================================
echo.

echo [1/8] Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado
    echo Descargue Python 3.8+ desde https://python.org
    pause
    exit /b 1
)
echo ✓ Python encontrado

echo.
echo [2/8] Creando directorio de produccion...
if not exist "C:\SisPla_Produccion" mkdir "C:\SisPla_Produccion"
cd /d "C:\SisPla_Produccion"
echo ✓ Directorio creado: C:\SisPla_Produccion

echo.
echo [3/8] Copiando archivos del sistema...
xcopy "C:\Cursor\SisPla_Phyton\*" "C:\SisPla_Produccion\" /E /I /Y
echo ✓ Archivos copiados

echo.
echo [4/8] Creando entorno virtual...
python -m venv venv
echo ✓ Entorno virtual creado

echo.
echo [5/8] Activando entorno virtual...
call venv\Scripts\activate.bat

echo.
echo [6/8] Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt
echo ✓ Dependencias instaladas

echo.
echo [7/8] Inicializando base de datos...
python sistema_final_funcional.py
echo ✓ Base de datos inicializada

echo.
echo [8/8] Creando script de inicio...
echo @echo off > iniciar_sistema.bat
echo echo Iniciando Sistema de Planillas... >> iniciar_sistema.bat
echo call venv\Scripts\activate.bat >> iniciar_sistema.bat
echo python app_completo.py >> iniciar_sistema.bat
echo pause >> iniciar_sistema.bat
echo ✓ Script de inicio creado

echo.
echo ========================================
echo INSTALACION COMPLETADA EXITOSAMENTE
echo ========================================
echo.
echo Para iniciar el sistema:
echo 1. Navegue a: C:\SisPla_Produccion
echo 2. Ejecute: iniciar_sistema.bat
echo 3. Abra su navegador en: http://localhost:5000
echo.
echo Para detener el sistema: Presione Ctrl+C
echo.
pause
