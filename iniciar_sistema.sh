#!/bin/bash

echo "========================================"
echo "Sistema de Planillas Multirégimen Perú"
echo "========================================"
echo

echo "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 no está instalado"
    echo "Por favor instale Python 3.7 o superior"
    exit 1
fi

echo "Python encontrado ✓"
echo

echo "Instalando dependencias..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron instalar las dependencias"
    exit 1
fi

echo "Dependencias instaladas ✓"
echo

echo "Inicializando base de datos..."
python3 init_db.py
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo inicializar la base de datos"
    exit 1
fi

echo "Base de datos inicializada ✓"
echo

echo "Ejecutando pruebas del sistema..."
python3 test_sistema.py
if [ $? -ne 0 ]; then
    echo "ADVERTENCIA: Las pruebas fallaron, pero el sistema puede funcionar"
    echo
fi

echo
echo "========================================"
echo "Sistema listo para usar"
echo "========================================"
echo
echo "Iniciando servidor web..."
echo "Abra su navegador en: http://localhost:5000"
echo
echo "Presione Ctrl+C para detener el servidor"
echo

python3 app.py

