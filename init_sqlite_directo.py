"""
Script de inicialización usando SQLite directamente - Sin SQLAlchemy
"""

import sqlite3
import os
from datetime import datetime, date

def crear_base_datos_directa():
    """Crea la base de datos usando SQLite directamente"""
    print("Creando base de datos usando SQLite directamente...")
    
    try:
        # Eliminar base de datos existente si hay problemas
        if os.path.exists('sispla.db'):
            os.remove('sispla.db')
            print("✓ Base de datos anterior eliminada")
        
        # Crear nueva base de datos
        conn = sqlite3.connect('sispla.db')
        cursor = conn.cursor()
        
        # Crear tabla empresas
        cursor.execute('''
            CREATE TABLE empresas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(200) NOT NULL,
                ruc VARCHAR(11) UNIQUE NOT NULL,
                regimen_laboral VARCHAR(50) NOT NULL,
                direccion VARCHAR(500),
                telefono VARCHAR(20),
                email VARCHAR(100),
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                activa BOOLEAN DEFAULT 1
            )
        ''')
        print("✓ Tabla empresas creada")
        
        # Crear tabla empleados
        cursor.execute('''
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
                activo BOOLEAN DEFAULT 1,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (empresa_id) REFERENCES empresas (id)
            )
        ''')
        print("✓ Tabla empleados creada")
        
        # Crear tabla locadores
        cursor.execute('''
            CREATE TABLE locadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                empresa_id INTEGER NOT NULL,
                nombres VARCHAR(100) NOT NULL,
                apellidos VARCHAR(100) NOT NULL,
                dni VARCHAR(8) NOT NULL,
                monto_mensual REAL NOT NULL,
                fecha_inicio DATE NOT NULL,
                fecha_fin DATE,
                direccion VARCHAR(500),
                telefono VARCHAR(20),
                email VARCHAR(100),
                suspendido BOOLEAN DEFAULT 0,
                activo BOOLEAN DEFAULT 1,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (empresa_id) REFERENCES empresas (id)
            )
        ''')
        print("✓ Tabla locadores creada")
        
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
        
        # Insertar datos de ejemplo
        cursor.execute('''
            INSERT INTO empresas (nombre, ruc, regimen_laboral, direccion, telefono, email)
            VALUES ('Empresa de Ejemplo S.A.C.', '20123456789', 'general', 'Av. Principal 123, Lima', '01-2345678', 'info@empresa-ejemplo.com')
        ''')
        print("✓ Empresa de ejemplo creada")
        
        empresa_id = cursor.lastrowid
        
        cursor.execute('''
            INSERT INTO empleados (empresa_id, nombres, apellidos, dni, sueldo_base, fecha_ingreso, fecha_nacimiento, direccion, telefono, email, tipo_pension)
            VALUES (?, 'Juan Carlos', 'Pérez García', '12345678', 1500.00, '2024-01-15', '1985-05-20', 'Jr. Los Olivos 456, Lima', '987654321', 'juan.perez@email.com', 'ONP')
        ''', (empresa_id,))
        print("✓ Empleado de ejemplo creado")
        
        cursor.execute('''
            INSERT INTO locadores (empresa_id, nombres, apellidos, dni, monto_mensual, fecha_inicio, direccion, telefono, email)
            VALUES (?, 'María Elena', 'Rodríguez López', '87654321', 2000.00, '2024-02-01', 'Av. Comercio 789, Lima', '912345678', 'maria.rodriguez@email.com')
        ''', (empresa_id,))
        print("✓ Locador de ejemplo creado")
        
        # Confirmar cambios
        conn.commit()
        conn.close()
        
        print("✓ Base de datos creada exitosamente usando SQLite directamente")
        return True
        
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        return False

def mostrar_resumen():
    """Muestra un resumen del sistema"""
    print("\n" + "="*60)
    print("SISTEMA DE PLANILLAS MULTIRÉGIMEN PERÚ")
    print("="*60)
    
    try:
        conn = sqlite3.connect('sispla.db')
        cursor = conn.cursor()
        
        # Contar registros
        cursor.execute('SELECT COUNT(*) FROM empresas')
        empresas_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM empleados')
        empleados_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM locadores')
        locadores_count = cursor.fetchone()[0]
        
        print(f"Empresas registradas: {empresas_count}")
        print(f"Empleados registrados: {empleados_count}")
        print(f"Locadores registrados: {locadores_count}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error mostrando resumen: {e}")
    
    print("\n" + "="*60)
    print("REGLAS DE NEGOCIO IMPLEMENTADAS:")
    print("="*60)
    
    reglas = {
        'microempresa': {
            'vacaciones': '15 días anuales',
            'cts': 'NO corresponde',
            'gratificaciones': 'NO corresponde',
            'asignacion_familiar': 'NO corresponde'
        },
        'pequeña_empresa': {
            'vacaciones': '15 días anuales',
            'cts': '15 días por año de servicio',
            'gratificaciones': 'Medio sueldo en Julio y Diciembre',
            'asignacion_familiar': 'S/. 102.50 (si sueldo ≤ S/. 1025)'
        },
        'general': {
            'vacaciones': '30 días anuales',
            'cts': 'Un sueldo anual',
            'gratificaciones': 'Sueldo + 9% en Julio y Diciembre',
            'asignacion_familiar': 'S/. 102.50 (si sueldo ≤ S/. 1025)'
        }
    }
    
    for regimen, beneficios in reglas.items():
        print(f"\n{regimen.upper()}:")
        for beneficio, descripcion in beneficios.items():
            print(f"  - {beneficio.title()}: {descripcion}")
    
    print("\n" + "="*60)
    print("DESCUENTOS APLICABLES:")
    print("="*60)
    print("- Pensión ONP: 13%")
    print("- Pensión AFP: 12% (según AFP)")
    print("- Impuesto a la Renta 5ta Cat.: Según tramos")
    print("- Retención 4ta Cat.: 8% (locadores, si monto > S/. 1,500)")
    
    print("\n" + "="*60)
    print("INSTRUCCIONES DE USO:")
    print("="*60)
    print("1. Ejecutar: python app_compatible.py")
    print("2. Abrir navegador en: http://localhost:5000")
    print("3. Crear empresas con diferentes regímenes laborales")
    print("4. Registrar empleados y locadores")
    print("5. Calcular planillas mensuales")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    try:
        if crear_base_datos_directa():
            mostrar_resumen()
        else:
            print("La inicialización falló. Revise los errores anteriores.")
    except Exception as e:
        print(f"Error general: {e}")
        import traceback
        traceback.print_exc()
