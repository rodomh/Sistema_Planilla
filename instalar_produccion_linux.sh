#!/bin/bash
echo "========================================"
echo "INSTALACION DEL SISTEMA DE PLANILLAS"
echo "========================================"
echo

echo "[1/8] Verificando Python..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python no esta instalado"
    echo "Instale Python 3.8+ con: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi
echo "✓ Python encontrado"

echo
echo "[2/8] Creando directorio de produccion..."
sudo mkdir -p /opt/sispla_produccion
sudo chown $USER:$USER /opt/sispla_produccion
cd /opt/sispla_produccion
echo "✓ Directorio creado: /opt/sispla_produccion"

echo
echo "[3/8] Copiando archivos del sistema..."
cp -r /path/to/SisPla_Phyton/* /opt/sispla_produccion/
echo "✓ Archivos copiados"

echo
echo "[4/8] Creando entorno virtual..."
python3 -m venv venv
echo "✓ Entorno virtual creado"

echo
echo "[5/8] Activando entorno virtual..."
source venv/bin/activate

echo
echo "[6/8] Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencias instaladas"

echo
echo "[7/8] Inicializando base de datos..."
python sistema_final_funcional.py
echo "✓ Base de datos inicializada"

echo
echo "[8/8] Creando script de inicio..."
cat > iniciar_sistema.sh << 'EOF'
#!/bin/bash
echo "Iniciando Sistema de Planillas..."
cd /opt/sispla_produccion
source venv/bin/activate
python app_completo.py
EOF
chmod +x iniciar_sistema.sh
echo "✓ Script de inicio creado"

echo
echo "========================================"
echo "INSTALACION COMPLETADA EXITOSAMENTE"
echo "========================================"
echo
echo "Para iniciar el sistema:"
echo "1. Ejecute: sudo /opt/sispla_produccion/iniciar_sistema.sh"
echo "2. Abra su navegador en: http://localhost:5000"
echo
echo "Para detener el sistema: Presione Ctrl+C"
echo
