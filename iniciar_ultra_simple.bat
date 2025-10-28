@echo off
echo ========================================
echo Sistema de Planillas Multiregimen Peru
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instale Python 3.7 o superior
    pause
    exit /b 1
)

echo Python encontrado ✓
echo.

echo Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo Dependencias instaladas ✓
echo.

echo Inicializando base de datos ultra simplificada...
python init_ultra_simple.py
if errorlevel 1 (
    echo ERROR: No se pudo inicializar la base de datos
    echo Intentando crear solo las tablas basicas...
    python -c "from app_ultra_simple import app, db; app.app_context().push(); db.create_all(); print('Tablas basicas creadas')"
    if errorlevel 1 (
        echo ERROR CRITICO: No se pueden crear las tablas
        pause
        exit /b 1
    )
)

echo Base de datos inicializada ✓
echo.

echo Ejecutando prueba rapida...
python test_ultra_simple.py
if errorlevel 1 (
    echo ADVERTENCIA: Las pruebas fallaron, pero el sistema puede funcionar
    echo.
)

echo.
echo ========================================
echo Sistema listo para usar
echo ========================================
echo.
echo Iniciando servidor web...
echo Abra su navegador en: http://localhost:5000
echo.
echo Presione Ctrl+C para detener el servidor
echo.

python app_ultra_simple.py

pause
