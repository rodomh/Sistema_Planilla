#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración para servidor de producción
"""

import os
import sys
from app_completo import app, db

def configurar_produccion():
    """Configurar el sistema para producción"""
    print("CONFIGURANDO SISTEMA PARA PRODUCCIÓN...")
    print("=" * 50)
    
    # Configuración de la aplicación
    app.config.update(
        DEBUG=False,
        TESTING=False,
        SECRET_KEY=os.urandom(24),
        SQLALCHEMY_DATABASE_URI='sqlite:///instance/database.db',
        UPLOAD_FOLDER='uploads',
        MAX_CONTENT_LENGTH=16 * 1024 * 1024  # 16MB max file size
    )
    
    # Crear directorios necesarios
    directorios = ['instance', 'uploads', 'backup', 'logs']
    for directorio in directorios:
        if not os.path.exists(directorio):
            os.makedirs(directorio)
            print(f"✓ Directorio creado: {directorio}")
    
    # Verificar base de datos
    try:
        with app.app_context():
            db.create_all()
            print("✓ Base de datos verificada")
    except Exception as e:
        print(f"❌ Error con base de datos: {e}")
        return False
    
    # Verificar archivos de plantillas
    plantillas = [
        'templates/base.html',
        'templates/index.html',
        'templates/empresas.html',
        'templates/personal.html',
        'templates/planilla_completo.html',
        'templates/nuevo_empleado_completo.html',
        'templates/nuevo_locador_completo.html',
        'templates/cargar_excel.html'
    ]
    
    for plantilla in plantillas:
        if os.path.exists(plantilla):
            print(f"✓ Plantilla encontrada: {plantilla}")
        else:
            print(f"❌ Plantilla faltante: {plantilla}")
            return False
    
    # Verificar archivos estáticos
    archivos_estaticos = [
        'static/css/bootstrap.min.css',
        'static/js/bootstrap.bundle.min.js',
        'static/css/style.css'
    ]
    
    for archivo in archivos_estaticos:
        if os.path.exists(archivo):
            print(f"✓ Archivo estático encontrado: {archivo}")
        else:
            print(f"⚠️  Archivo estático faltante: {archivo}")
    
    print("\n" + "=" * 50)
    print("✅ CONFIGURACIÓN COMPLETADA")
    print("=" * 50)
    print("🎯 SISTEMA LISTO PARA PRODUCCIÓN")
    print("   - Debug: DESHABILITADO")
    print("   - Base de datos: SQLite")
    print("   - Directorios: Creados")
    print("   - Archivos: Verificados")
    print("\nPara iniciar el servidor:")
    print("   python app_completo.py")
    print("\nPara acceso:")
    print("   http://localhost:5000")
    print("   http://[IP_SERVIDOR]:5000")
    
    return True

if __name__ == "__main__":
    configurar_produccion()
