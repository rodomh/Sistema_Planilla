"""
Script para corregir las importaciones de db en todos los archivos
"""

import re

def corregir_archivo(archivo):
    """Corrige las importaciones de db en un archivo"""
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Agregar importación de db en funciones que la usan
    funciones_con_db = [
        'obtener_ausencias_empresa',
        'calcular_dias_trabajados_mes', 
        'obtener_resumen_ausencias_empresa',
        'justificar_ausencia',
        'eliminar_ausencia',
        'obtener_estadisticas_ausencias',
        'crear_prestamo',
        'crear_adelanto',
        'obtener_prestamos_empleado',
        'obtener_adelantos_empleado',
        'obtener_deudas_empresa',
        'procesar_pago_prestamo',
        'calcular_cuota_prestamo',
        'obtener_resumen_deudas_empleado',
        'cancelar_prestamo',
        'cancelar_adelanto',
        'obtener_historial_pagos_empleado',
        'validar_capacidad_pago'
    ]
    
    for funcion in funciones_con_db:
        # Buscar la función y agregar importación de db
        patron = f'(def {funcion}\\(.*?\\):)\n(    """.*?""")'
        reemplazo = r'\1\n    from app import db\n\2'
        contenido = re.sub(patron, reemplazo, contenido, flags=re.DOTALL)
    
    # También corregir referencias directas a db.session
    contenido = re.sub(r'\bdb\.session\.', 'db.session.', contenido)
    
    with open(archivo, 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    print(f"✓ Corregido: {archivo}")

# Corregir archivos
archivos = ['gestion_personal.py', 'gestion_deudas.py']
for archivo in archivos:
    try:
        corregir_archivo(archivo)
    except Exception as e:
        print(f"Error corrigiendo {archivo}: {e}")

print("Corrección completada")
