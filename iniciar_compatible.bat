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

echo Instalando dependencias compatibles...
pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5 SQLAlchemy==1.4.53 Werkzeug==2.3.7 Jinja2==3.1.2
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo Dependencias instaladas ✓
echo.

echo Creando base de datos usando SQLite directamente...
python init_sqlite_directo.py
if errorlevel 1 (
    echo ERROR: No se pudo crear la base de datos
    pause
    exit /b 1
)

echo Base de datos creada ✓
echo.

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

python app_compatible.py

pause
