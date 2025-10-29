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

echo Verificando base de datos...
if exist sispla.db (
    echo Base de datos existente encontrada
    echo Actualizando con nuevas tablas y campos...
    python actualizar_bd.py
    if errorlevel 1 (
        echo ERROR: No se pudo actualizar las tablas
        pause
        exit /b 1
    )
    echo Actualizando campos bancarios y tipo de pago...
    python actualizar_campos_bancarios.py
    if errorlevel 1 (
        echo ERROR: No se pudo actualizar los campos bancarios
        pause
        exit /b 1
    )
    echo Base de datos actualizada ✓
) else (
    echo Creando nueva base de datos...
    python init_sqlite_directo.py
    if errorlevel 1 (
        echo ERROR: No se pudo crear la base de datos
        pause
        exit /b 1
    )
    echo Base de datos creada ✓
)

echo.

echo Probando rutas del sistema...
python test_rutas.py
if errorlevel 1 (
    echo ADVERTENCIA: Las pruebas fallaron, pero el sistema puede funcionar
    echo.
)

echo.
echo ========================================
echo Sistema listo para usar
echo ========================================
echo.
echo FUNCIONALIDADES DISPONIBLES:
echo - Gestión de empresas con diferentes regímenes laborales
echo - Gestión de empleados y locadores con información bancaria
echo - Control de ausencias (faltas, permisos, vacaciones)
echo - Gestión de préstamos y adelantos
echo - Cálculo de planillas con pago mensual/quincenal
echo - Descuentos automáticos por ausencias y deudas
echo.
echo NUEVAS MEJORAS:
echo - Campos bancarios para empleados y locadores
echo - Tipo de pago: mensual (100%%) o quincenal (50%%)
echo - Conteo correcto de empleados activos
echo - Manual completo de funcionamiento
echo.
echo Iniciando servidor web...
echo Abra su navegador en: http://localhost:5000
echo.
echo Presione Ctrl+C para detener el servidor
echo.

python app_compatible.py

pause
