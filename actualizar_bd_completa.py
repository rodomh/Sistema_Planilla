#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Actualizar base de datos con todas las funcionalidades completas
"""

import sqlite3
import os

def actualizar_bd_completa():
    """Actualizar base de datos con todas las funcionalidades"""
    print("ACTUALIZANDO BASE DE DATOS COMPLETA...")
    print("=" * 50)
    
    # Conectar a la base de datos
    conn = sqlite3.connect('planillas_peru.db')
    cursor = conn.cursor()
    
    try:
        # Verificar si las columnas ya existen
        cursor.execute("PRAGMA table_info(empleados)")
        empleados_columns = [column[1] for column in cursor.fetchall()]
        
        cursor.execute("PRAGMA table_info(locadores)")
        locadores_columns = [column[1] for column in cursor.fetchall()]
        
        # Agregar columnas a empleados si no existen
        if 'cuenta_bancaria' not in empleados_columns:
            cursor.execute("ALTER TABLE empleados ADD COLUMN cuenta_bancaria VARCHAR(20)")
            print("✓ Agregada columna cuenta_bancaria a empleados")
        
        if 'banco' not in empleados_columns:
            cursor.execute("ALTER TABLE empleados ADD COLUMN banco VARCHAR(50)")
            print("✓ Agregada columna banco a empleados")
        
        if 'tipo_pago' not in empleados_columns:
            cursor.execute("ALTER TABLE empleados ADD COLUMN tipo_pago VARCHAR(20) DEFAULT 'mensual'")
            print("✓ Agregada columna tipo_pago a empleados")
        
        if 'descuento_alimentos' not in empleados_columns:
            cursor.execute("ALTER TABLE empleados ADD COLUMN descuento_alimentos REAL DEFAULT 0.0")
            print("✓ Agregada columna descuento_alimentos a empleados")
        
        # Agregar columnas a locadores si no existen
        if 'cuenta_bancaria' not in locadores_columns:
            cursor.execute("ALTER TABLE locadores ADD COLUMN cuenta_bancaria VARCHAR(20)")
            print("✓ Agregada columna cuenta_bancaria a locadores")
        
        if 'banco' not in locadores_columns:
            cursor.execute("ALTER TABLE locadores ADD COLUMN banco VARCHAR(50)")
            print("✓ Agregada columna banco a locadores")
        
        if 'descuento_alimentos' not in locadores_columns:
            cursor.execute("ALTER TABLE locadores ADD COLUMN descuento_alimentos REAL DEFAULT 0.0")
            print("✓ Agregada columna descuento_alimentos a locadores")
        
        # Crear tablas de ausencias, préstamos y adelantos si no existen
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ausencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                empleado_id INTEGER NOT NULL,
                fecha DATE NOT NULL,
                tipo VARCHAR(20) NOT NULL,
                motivo VARCHAR(500),
                horas_perdidas REAL DEFAULT 0.0,
                FOREIGN KEY (empleado_id) REFERENCES empleados (id)
            )
        """)
        print("✓ Tabla ausencias creada/verificada")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prestamos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                empleado_id INTEGER NOT NULL,
                monto REAL NOT NULL,
                cuotas INTEGER NOT NULL,
                cuota_mensual REAL NOT NULL,
                cuotas_pagadas INTEGER DEFAULT 0,
                fecha_inicio DATE NOT NULL,
                activo BOOLEAN DEFAULT 1,
                FOREIGN KEY (empleado_id) REFERENCES empleados (id)
            )
        """)
        print("✓ Tabla prestamos creada/verificada")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS adelantos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                empleado_id INTEGER NOT NULL,
                monto REAL NOT NULL,
                fecha DATE NOT NULL,
                descuento_mensual REAL NOT NULL,
                meses_restantes INTEGER NOT NULL,
                activo BOOLEAN DEFAULT 1,
                FOREIGN KEY (empleado_id) REFERENCES empleados (id)
            )
        """)
        print("✓ Tabla adelantos creada/verificada")
        
        # Confirmar cambios
        conn.commit()
        
        print("\n" + "=" * 50)
        print("✅ BASE DE DATOS ACTUALIZADA EXITOSAMENTE")
        print("=" * 50)
        print("📊 Funcionalidades agregadas:")
        print("   ✓ Campos bancarios (cuenta_bancaria, banco)")
        print("   ✓ Tipo de pago (mensual/quincenal)")
        print("   ✓ Descuento por alimentos")
        print("   ✓ Tablas de ausencias, préstamos y adelantos")
        print("   ✓ Sistema listo para funcionalidades completas")
        
    except Exception as e:
        print(f"❌ Error al actualizar base de datos: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    actualizar_bd_completa()
