@echo off
title Sistema de Planillas - Produccion
echo ========================================
echo    SISTEMA DE PLANILLAS - PRODUCCION
echo ========================================
echo.
echo Iniciando sistema...
echo.

REM Verificar si existe el entorno virtual
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Entorno virtual no encontrado
    echo Ejecute primero: instalar_produccion.bat
    pause
    exit /b 1
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Verificar Python
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python no encontrado
    pause
    exit /b 1
)

REM Verificar archivos necesarios
if not exist "app_completo.py" (
    echo ERROR: app_completo.py no encontrado
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ERROR: requirements.txt no encontrado
    pause
    exit /b 1
)

REM Crear directorios necesarios
if not exist "instance" mkdir instance
if not exist "uploads" mkdir uploads
if not exist "backup" mkdir backup
if not exist "logs" mkdir logs

echo.
echo ========================================
echo    INICIANDO SERVIDOR...
echo ========================================
echo.
echo Sistema accesible en:
echo   - Local:    http://localhost:5000
echo   - Red:      http://[IP_SERVIDOR]:5000
echo.
echo Para detener: Presione Ctrl+C
echo.

REM Iniciar aplicación
python app_completo.py

echo.
echo Sistema detenido.
pause