"""
Script para actualizar la base de datos existente con las nuevas tablas
"""

import sqlite3
import os
from datetime import datetime, date

def actualizar_base_datos():
    """Actualiza la base de datos existente con las nuevas tablas"""
    print("Actualizando base de datos con nuevas tablas...")
    
    try:
        # Conectar a la base de datos existente
        conn = sqlite3.connect('sispla.db')
        cursor = conn.cursor()
        
        # Verificar si las tablas ya existen
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ausencias'")
        if cursor.fetchone():
            print("✓ Tabla ausencias ya existe")
        else:
            # Crear tabla ausencias
            cursor.execute('''
                CREATE TABLE ausencias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    empleado_id INTEGER NOT NULL,
                    fecha DATE NOT NULL,
                    tipo VARCHAR(20) NOT NULL,
                    justificada BOOLEAN DEFAULT 0,
                    motivo VARCHAR(500),
                    horas_perdidas REAL DEFAULT 8.0,
                    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (empleado_id) REFERENCES empleados (id)
                )
            ''')
            print("✓ Tabla ausencias creada")
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='prestamos'")
        if cursor.fetchone():
            print("✓ Tabla prestamos ya existe")
        else:
            # Crear tabla prestamos
            cursor.execute('''
                CREATE TABLE prestamos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    empleado_id INTEGER NOT NULL,
                    monto_total REAL NOT NULL,
                    monto_pendiente REAL NOT NULL,
                    cuota_mensual REAL NOT NULL,
                    fecha_prestamo DATE NOT NULL,
                    fecha_finalizacion DATE,
                    motivo VARCHAR(500),
                    activo BOOLEAN DEFAULT 1,
                    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (empleado_id) REFERENCES empleados (id)
                )
            ''')
            print("✓ Tabla prestamos creada")
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='adelantos'")
        if cursor.fetchone():
            print("✓ Tabla adelantos ya existe")
        else:
            # Crear tabla adelantos
            cursor.execute('''
                CREATE TABLE adelantos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    empleado_id INTEGER NOT NULL,
                    monto REAL NOT NULL,
                    fecha_adelanto DATE NOT NULL,
                    mes_aplicar INTEGER NOT NULL,
                    año_aplicar INTEGER NOT NULL,
                    motivo VARCHAR(500),
                    aplicado BOOLEAN DEFAULT 0,
                    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (empleado_id) REFERENCES empleados (id)
                )
            ''')
            print("✓ Tabla adelantos creada")
        
        # Confirmar cambios
        conn.commit()
        conn.close()
        
        print("✓ Base de datos actualizada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando base de datos: {e}")
        return False

def mostrar_resumen():
    """Muestra un resumen de las tablas disponibles"""
    print("\n" + "="*60)
    print("TABLAS DISPONIBLES EN LA BASE DE DATOS")
    print("="*60)
    
    try:
        conn = sqlite3.connect('sispla.db')
        cursor = conn.cursor()
        
        # Listar todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = cursor.fetchall()
        
        print(f"Total de tablas: {len(tablas)}")
        for tabla in tablas:
            print(f"  - {tabla[0]}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error mostrando resumen: {e}")
    
    print("\n" + "="*60)
    print("FUNCIONALIDADES DISPONIBLES:")
    print("="*60)
    print("✅ Gestión de empresas")
    print("✅ Gestión de empleados y locadores")
    print("✅ Control de ausencias")
    print("✅ Gestión de préstamos")
    print("✅ Gestión de adelantos")
    print("✅ Cálculo de planillas con descuentos automáticos")
    
    print("\n" + "="*60)
    print("INSTRUCCIONES:")
    print("="*60)
    print("1. Ejecutar: python app_compatible.py")
    print("2. Abrir navegador en: http://localhost:5000")
    print("3. Las nuevas funcionalidades están disponibles en el menú")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    try:
        if actualizar_base_datos():
            mostrar_resumen()
        else:
            print("La actualización falló. Revise los errores anteriores.")
    except Exception as e:
        print(f"Error general: {e}")
        import traceback
        traceback.print_exc()
