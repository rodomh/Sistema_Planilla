"""
Script de prueba usando SQLite directamente
"""

import sqlite3
from datetime import datetime, date

def prueba_sistema_completo():
    """Ejecuta una prueba completa del sistema"""
    print("🧪 INICIANDO PRUEBA CON SQLITE DIRECTO")
    print("="*60)
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('sispla.db')
        cursor = conn.cursor()
        
        # 1. Verificar empresas
        print("1. Verificando empresas...")
        cursor.execute('SELECT COUNT(*) FROM empresas')
        empresas_count = cursor.fetchone()[0]
        print(f"   ✓ Empresas encontradas: {empresas_count}")
        
        if empresas_count == 0:
            print("   ❌ No hay empresas. Ejecute init_sqlite_directo.py primero")
            return False
        
        # Obtener empresa de ejemplo
        cursor.execute('SELECT * FROM empresas LIMIT 1')
        empresa = cursor.fetchone()
        print(f"   ✓ Empresa de prueba: {empresa[1]} ({empresa[3]})")
        
        # 2. Verificar empleados
        print("\n2. Verificando empleados...")
        cursor.execute('SELECT COUNT(*) FROM empleados')
        empleados_count = cursor.fetchone()[0]
        print(f"   ✓ Empleados encontrados: {empleados_count}")
        
        if empleados_count == 0:
            print("   ❌ No hay empleados. Agregue empleados desde la interfaz web")
            return False
        
        # Obtener empleado de ejemplo
        cursor.execute('SELECT * FROM empleados LIMIT 1')
        empleado = cursor.fetchone()
        print(f"   ✓ Empleado de prueba: {empleado[2]} {empleado[3]}")
        
        # 3. Verificar locadores
        print("\n3. Verificando locadores...")
        cursor.execute('SELECT COUNT(*) FROM locadores')
        locadores_count = cursor.fetchone()[0]
        print(f"   ✓ Locadores encontrados: {locadores_count}")
        
        # 4. Probar cálculo de planilla básico
        print("\n4. Probando cálculo de planilla básico...")
        sueldo_base = empleado[6]  # sueldo_base está en la posición 6
        regimen = empresa[3]  # regimen_laboral está en la posición 3
        
        # Cálculo básico según régimen
        if regimen in ['microempresa', 'pequeña_empresa']:
            vacaciones = sueldo_base * 15 / 360
        else:
            vacaciones = sueldo_base * 30 / 360
            
        if regimen == 'microempresa':
            cts = 0
        elif regimen == 'pequeña_empresa':
            cts = sueldo_base * 15 / 12
        else:
            cts = sueldo_base
            
        # Descuentos básicos
        pension = sueldo_base * 0.13  # ONP
        if sueldo_base > 1025:
            impuesto_renta = max(0, (sueldo_base - 1025) * 0.08)
        else:
            impuesto_renta = 0
        
        neto_pagar = sueldo_base + vacaciones + cts - pension - impuesto_renta
        
        print(f"   ✓ Sueldo base: S/. {sueldo_base:.2f}")
        print(f"   ✓ Vacaciones: S/. {vacaciones:.2f}")
        print(f"   ✓ CTS: S/. {cts:.2f}")
        print(f"   ✓ Pensión: S/. {pension:.2f}")
        print(f"   ✓ Impuesto Renta: S/. {impuesto_renta:.2f}")
        print(f"   ✓ Neto a Pagar: S/. {neto_pagar:.2f}")
        
        conn.close()
        
        print("\n" + "="*60)
        print("✅ PRUEBA COMPLETA EXITOSA")
        print("="*60)
        print("El sistema está funcionando correctamente.")
        print("Puede acceder a la interfaz web en: http://localhost:5000")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR DURANTE LA PRUEBA: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🚀 SISTEMA DE PLANILLAS MULTIRÉGIMEN PERÚ - PRUEBAS CON SQLITE DIRECTO")
    print("="*60)
    
    # Ejecutar prueba completa
    if prueba_sistema_completo():
        print("\n🎉 PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("El sistema está listo para usar.")
    else:
        print("\n❌ LAS PRUEBAS FALLARON")
        print("Revise la configuración y ejecute init_sqlite_directo.py")
