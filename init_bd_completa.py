#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inicializar base de datos completa con todas las funcionalidades
"""

import sqlite3
import os
from datetime import datetime, date

def init_bd_completa():
    """Crear base de datos completa con todas las funcionalidades"""
    print("INICIALIZANDO BASE DE DATOS COMPLETA...")
    print("=" * 60)
    
    # Eliminar base de datos existente si existe
    if os.path.exists('planillas_peru.db'):
        os.remove('planillas_peru.db')
        print("✓ Base de datos anterior eliminada")
    
    # Conectar a la base de datos
    conn = sqlite3.connect('planillas_peru.db')
    cursor = conn.cursor()
    
    try:
        # Crear tabla empresas
        cursor.execute("""
            CREATE TABLE empresas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(200) NOT NULL,
                ruc VARCHAR(11) UNIQUE NOT NULL,
                regimen_laboral VARCHAR(50) NOT NULL,
                direccion VARCHAR(500),
                telefono VARCHAR(20),
                email VARCHAR(100),
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Tabla empresas creada")
        
        # Crear tabla empleados con todas las columnas
        cursor.execute("""
            CREATE TABLE empleados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                empresa_id INTEGER NOT NULL,
                nombres VARCHAR(100) NOT NULL,
                apellidos VARCHAR(100) NOT NULL,
                dni VARCHAR(8) NOT NULL,
                sueldo_base REAL NOT NULL,
                fecha_ingreso DATE NOT NULL,
                fecha_nacimiento DATE,
                direccion VARCHAR(500),
                telefono VARCHAR(20),
                email VARCHAR(100),
                tipo_pension VARCHAR(20) DEFAULT 'ONP',
                afp_codigo VARCHAR(10),
                cuenta_bancaria VARCHAR(20),
                banco VARCHAR(50),
                tipo_pago VARCHAR(20) DEFAULT 'mensual',
                descuento_alimentos REAL DEFAULT 0.0,
                activo BOOLEAN DEFAULT 1,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (empresa_id) REFERENCES empresas (id)
            )
        """)
        print("✓ Tabla empleados creada con todas las columnas")
        
        # Crear tabla locadores con todas las columnas
        cursor.execute("""
            CREATE TABLE locadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                empresa_id INTEGER NOT NULL,
                nombres VARCHAR(100) NOT NULL,
                apellidos VARCHAR(100) NOT NULL,
                dni VARCHAR(8) NOT NULL,
                monto_mensual REAL NOT NULL,
                fecha_inicio DATE NOT NULL,
                suspendido BOOLEAN DEFAULT 0,
                cuenta_bancaria VARCHAR(20),
                banco VARCHAR(50),
                descuento_alimentos REAL DEFAULT 0.0,
                activo BOOLEAN DEFAULT 1,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (empresa_id) REFERENCES empresas (id)
            )
        """)
        print("✓ Tabla locadores creada con todas las columnas")
        
        # Crear tabla ausencias
        cursor.execute("""
            CREATE TABLE ausencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                empleado_id INTEGER NOT NULL,
                fecha DATE NOT NULL,
                tipo VARCHAR(20) NOT NULL,
                motivo VARCHAR(500),
                horas_perdidas REAL DEFAULT 0.0,
                FOREIGN KEY (empleado_id) REFERENCES empleados (id)
            )
        """)
        print("✓ Tabla ausencias creada")
        
        # Crear tabla prestamos
        cursor.execute("""
            CREATE TABLE prestamos (
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
        print("✓ Tabla prestamos creada")
        
        # Crear tabla adelantos
        cursor.execute("""
            CREATE TABLE adelantos (
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
        print("✓ Tabla adelantos creada")
        
        # Crear datos de ejemplo
        print("\n📊 CREANDO DATOS DE EJEMPLO...")
        
        # Empresas
        empresas_data = [
            ('Inversiones IH SRL', '20123456789', 'microempresa', 'Av. Principal 123, Lima', '987654321', 'info@inversionesih.com'),
            ('Servicios Generales SAC', '20234567890', 'pequeña_empresa', 'Jr. Comercio 456, Lima', '987654322', 'info@serviciosgenerales.com'),
            ('Corporación Empresarial S.A.C.', '20345678901', 'general', 'Av. Industrial 789, Lima', '987654323', 'info@corporacionempresarial.com')
        ]
        
        for empresa_data in empresas_data:
            cursor.execute("""
                INSERT INTO empresas (nombre, ruc, regimen_laboral, direccion, telefono, email)
                VALUES (?, ?, ?, ?, ?, ?)
            """, empresa_data)
        
        print("✓ 3 empresas creadas")
        
        # Empleados
        empleados_data = [
            # Microempresa
            (1, 'Juan Carlos', 'Pérez García', '12345678', 1500.0, '2024-01-15', '1990-05-20', 'Av. Lima 123', '987654321', 'juan@email.com', 'ONP', None, '1234567890123456', 'BCP', 'mensual', 0.0),
            (1, 'María Elena', 'López Silva', '87654321', 2000.0, '2024-02-01', '1985-08-15', 'Jr. Paz 456', '987654322', 'maria@email.com', 'AFP', 'PRIMA', '9876543210987654', 'BBVA', 'quincenal', 200.0),
            # Pequeña Empresa
            (2, 'Carlos', 'Mendoza Vega', '11223344', 1800.0, '2024-03-10', '1988-12-10', 'Av. Comercio 789', '987654323', 'carlos@email.com', 'ONP', None, '1122334455667788', 'SCOTIABANK', 'mensual', 150.0),
            # Régimen General
            (3, 'Ana María', 'Rodríguez Castro', '55667788', 2500.0, '2024-01-20', '1982-03-25', 'Av. Industrial 321', '987654324', 'ana@email.com', 'AFP', 'PROFUTURO', '5566778899001122', 'INTERBANK', 'mensual', 300.0)
        ]
        
        for emp_data in empleados_data:
            cursor.execute("""
                INSERT INTO empleados (empresa_id, nombres, apellidos, dni, sueldo_base, fecha_ingreso, 
                                    fecha_nacimiento, direccion, telefono, email, tipo_pension, afp_codigo,
                                    cuenta_bancaria, banco, tipo_pago, descuento_alimentos)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, emp_data)
        
        print("✓ 4 empleados creados")
        
        # Locadores
        locadores_data = [
            (1, 'Luis', 'Herrera Morales', '99887766', 3000.0, '2024-02-15', 0, '9988776655443322', 'BCP', 250.0),
            (2, 'Elena', 'Díaz Paz', '44332211', 2800.0, '2024-03-05', 0, '4433221100998877', 'BBVA', 0.0),
            (3, 'Roberto', 'Sánchez Torres', '77889900', 4000.0, '2024-01-10', 1, '7788990011223344', 'SCOTIABANK', 400.0)
        ]
        
        for loc_data in locadores_data:
            cursor.execute("""
                INSERT INTO locadores (empresa_id, nombres, apellidos, dni, monto_mensual, fecha_inicio,
                                     suspendido, cuenta_bancaria, banco, descuento_alimentos)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, loc_data)
        
        print("✓ 3 locadores creados")
        
        # Confirmar cambios
        conn.commit()
        
        print("\n" + "=" * 60)
        print("✅ BASE DE DATOS COMPLETA INICIALIZADA EXITOSAMENTE")
        print("=" * 60)
        print("📊 Estructura creada:")
        print("   ✓ Tabla empresas (3 registros)")
        print("   ✓ Tabla empleados (4 registros con todas las columnas)")
        print("   ✓ Tabla locadores (3 registros con todas las columnas)")
        print("   ✓ Tabla ausencias")
        print("   ✓ Tabla prestamos")
        print("   ✓ Tabla adelantos")
        print("\n🎯 Funcionalidades disponibles:")
        print("   ✓ Tipos de pago (mensual/quincenal)")
        print("   ✓ Descuentos por alimentos")
        print("   ✓ Información bancaria")
        print("   ✓ Cálculo de planillas por régimen")
        print("   ✓ Exportación a Excel")
        print("   ✓ Gestión completa de personal")
        
    except Exception as e:
        print(f"❌ Error al inicializar base de datos: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    init_bd_completa()
