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
            print("OK: Campo cuenta_bancaria agregado a empleados")
        else:
            print("OK: Campo cuenta_bancaria ya existe en empleados")
        
        if 'banco' not in empleados_columns:
            cursor.execute('ALTER TABLE empleados ADD COLUMN banco VARCHAR(50)')
            print("OK: Campo banco agregado a empleados")
        else:
            print("OK: Campo banco ya existe en empleados")
        
        if 'tipo_pago' not in empleados_columns:
            cursor.execute('ALTER TABLE empleados ADD COLUMN tipo_pago VARCHAR(20) DEFAULT "mensual"')
            print("OK: Campo tipo_pago agregado a empleados")
        else:
            print("OK: Campo tipo_pago ya existe en empleados")
        
        # Verificar si los campos ya existen en locadores
        cursor.execute("PRAGMA table_info(locadores)")
        locadores_columns = [column[1] for column in cursor.fetchall()]
        
        if 'cuenta_bancaria' not in locadores_columns:
            cursor.execute('ALTER TABLE locadores ADD COLUMN cuenta_bancaria VARCHAR(20)')
            print("OK: Campo cuenta_bancaria agregado a locadores")
        else:
            print("OK: Campo cuenta_bancaria ya existe en locadores")
        
        if 'banco' not in locadores_columns:
            cursor.execute('ALTER TABLE locadores ADD COLUMN banco VARCHAR(50)')
            print("OK: Campo banco agregado a locadores")
        else:
            print("OK: Campo banco ya existe en locadores")
        
        # Confirmar cambios
        conn.commit()
        conn.close()
        
        print("OK: Base de datos actualizada exitosamente con campos bancarios")
        return True
        
    except Exception as e:
        print(f"ERROR: Error actualizando campos bancarios: {e}")
        return False

def mostrar_resumen():
    """Muestra un resumen de las mejoras implementadas"""
    print("\n" + "="*60)
    print("MEJORAS IMPLEMENTADAS EN EL SISTEMA")
    print("="*60)
    
    print("\nOK: CAMPOS BANCARIOS AGREGADOS:")
    print("  - Cuenta bancaria para empleados y locadores")
    print("  - Seleccion de banco principal")
    print("  - Informacion visible en planillas")
    
    print("\nOK: TIPO DE PAGO IMPLEMENTADO:")
    print("  - Pago mensual (100% del sueldo)")
    print("  - Pago quincenal (50% del sueldo)")
    print("  - Calculo automatico segun tipo seleccionado")
    
    print("\nOK: CONTEO CORREGIDO:")
    print("  - Solo cuenta empleados y locadores activos")
    print("  - Conteo preciso en ventana inicial")
    
    print("\nOK: MANUAL DE FUNCIONAMIENTO:")
    print("  - Documentacion completa del calculo de planilla")
    print("  - Ejemplos paso a paso")
    print("  - Explicacion de todos los regímenes laborales")
    
    print("\n" + "="*60)
    print("BANCOS SOPORTADOS:")
    print("="*60)
    bancos = [
        "Banco de Credito del Peru (BCP)",
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
    print("3. Crear/editar empleados con informacion bancaria")
    print("4. Seleccionar tipo de pago (mensual/quincenal)")
    print("5. Calcular planillas con descuentos automaticos")
    print("6. Consultar manual: MANUAL_CALCULO_PLANILLA.md")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    try:
        if actualizar_campos_bancarios():
            mostrar_resumen()
        else:
            print("La actualizacion fallo. Revise los errores anteriores.")
    except Exception as e:
        print(f"Error general: {e}")
        import traceback
        traceback.print_exc()
