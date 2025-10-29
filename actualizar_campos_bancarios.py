"""
Script para actualizar la base de datos con los nuevos campos bancarios y tipo de pago
"""

import sqlite3
import os
from datetime import datetime, date

def actualizar_campos_bancarios():
    """Actualiza la base de datos con los nuevos campos bancarios y tipo de pago"""
    print("Actualizando base de datos con campos bancarios y tipo de pago...")
    
    try:
        # Conectar a la base de datos existente
        conn = sqlite3.connect('sispla.db')
        cursor = conn.cursor()
        
        # Verificar si los campos ya existen en empleados
        cursor.execute("PRAGMA table_info(empleados)")
        empleados_columns = [column[1] for column in cursor.fetchall()]
        
        if 'cuenta_bancaria' not in empleados_columns:
            cursor.execute('ALTER TABLE empleados ADD COLUMN cuenta_bancaria VARCHAR(20)')
            print("✓ Campo cuenta_bancaria agregado a empleados")
        else:
            print("✓ Campo cuenta_bancaria ya existe en empleados")
        
        if 'banco' not in empleados_columns:
            cursor.execute('ALTER TABLE empleados ADD COLUMN banco VARCHAR(50)')
            print("✓ Campo banco agregado a empleados")
        else:
            print("✓ Campo banco ya existe en empleados")
        
        if 'tipo_pago' not in empleados_columns:
            cursor.execute('ALTER TABLE empleados ADD COLUMN tipo_pago VARCHAR(20) DEFAULT "mensual"')
            print("✓ Campo tipo_pago agregado a empleados")
        else:
            print("✓ Campo tipo_pago ya existe en empleados")
        
        # Verificar si los campos ya existen en locadores
        cursor.execute("PRAGMA table_info(locadores)")
        locadores_columns = [column[1] for column in cursor.fetchall()]
        
        if 'cuenta_bancaria' not in locadores_columns:
            cursor.execute('ALTER TABLE locadores ADD COLUMN cuenta_bancaria VARCHAR(20)')
            print("✓ Campo cuenta_bancaria agregado a locadores")
        else:
            print("✓ Campo cuenta_bancaria ya existe en locadores")
        
        if 'banco' not in locadores_columns:
            cursor.execute('ALTER TABLE locadores ADD COLUMN banco VARCHAR(50)')
            print("✓ Campo banco agregado a locadores")
        else:
            print("✓ Campo banco ya existe en locadores")
        
        # Confirmar cambios
        conn.commit()
        conn.close()
        
        print("✓ Base de datos actualizada exitosamente con campos bancarios")
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando campos bancarios: {e}")
        return False

def mostrar_resumen():
    """Muestra un resumen de las mejoras implementadas"""
    print("\n" + "="*60)
    print("MEJORAS IMPLEMENTADAS EN EL SISTEMA")
    print("="*60)
    
    print("\n✅ CAMPOS BANCARIOS AGREGADOS:")
    print("  - Cuenta bancaria para empleados y locadores")
    print("  - Selección de banco principal")
    print("  - Información visible en planillas")
    
    print("\n✅ TIPO DE PAGO IMPLEMENTADO:")
    print("  - Pago mensual (100% del sueldo)")
    print("  - Pago quincenal (50% del sueldo)")
    print("  - Cálculo automático según tipo seleccionado")
    
    print("\n✅ CONTEO CORREGIDO:")
    print("  - Solo cuenta empleados y locadores activos")
    print("  - Conteo preciso en ventana inicial")
    
    print("\n✅ MANUAL DE FUNCIONAMIENTO:")
    print("  - Documentación completa del cálculo de planilla")
    print("  - Ejemplos paso a paso")
    print("  - Explicación de todos los regímenes laborales")
    
    print("\n" + "="*60)
    print("BANCOS SOPORTADOS:")
    print("="*60)
    bancos = [
        "Banco de Crédito del Perú (BCP)",
        "BBVA Continental",
        "Scotiabank",
        "Interbank",
        "BanBif",
        "Banco Pichincha",
        "Otro"
    ]
    for banco in bancos:
        print(f"  - {banco}")
    
    print("\n" + "="*60)
    print("INSTRUCCIONES DE USO:")
    print("="*60)
    print("1. Ejecutar: python app_compatible.py")
    print("2. Abrir navegador en: http://localhost:5000")
    print("3. Crear/editar empleados con información bancaria")
    print("4. Seleccionar tipo de pago (mensual/quincenal)")
    print("5. Calcular planillas con descuentos automáticos")
    print("6. Consultar manual: MANUAL_CALCULO_PLANILLA.md")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    try:
        if actualizar_campos_bancarios():
            mostrar_resumen()
        else:
            print("La actualización falló. Revise los errores anteriores.")
    except Exception as e:
        print(f"Error general: {e}")
        import traceback
        traceback.print_exc()
