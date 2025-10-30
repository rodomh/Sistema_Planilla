#!/bin/bash
echo "========================================"
echo "   SISTEMA DE PLANILLAS - PRODUCCION"
echo "========================================"
echo
echo "Iniciando sistema..."
echo

# Verificar si existe el entorno virtual
if [ ! -f "venv/bin/activate" ]; then
    echo "ERROR: Entorno virtual no encontrado"
    echo "Ejecute primero: ./instalar_produccion_linux.sh"
    exit 1
fi

# Activar entorno virtual
source venv/bin/activate

# Verificar Python
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python no encontrado"
    exit 1
fi

# Verificar archivos necesarios
if [ ! -f "app_completo.py" ]; then
    echo "ERROR: app_completo.py no encontrado"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "ERROR: requirements.txt no encontrado"
    exit 1
fi

# Crear directorios necesarios
mkdir -p instance uploads backup logs

echo
echo "========================================"
echo "   INICIANDO SERVIDOR..."
echo "========================================"
echo
echo "Sistema accesible en:"
echo "  - Local:    http://localhost:5000"
echo "  - Red:      http://[IP_SERVIDOR]:5000"
echo
echo "Para detener: Presione Ctrl+C"
echo

# Iniciar aplicación
python3 app_completo.py

echo
echo "Sistema detenido."