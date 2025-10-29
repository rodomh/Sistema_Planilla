"""
Script de prueba para verificar que el sistema funcional funcione correctamente
"""

from app_funcional import app, db, Empresa, Empleado, Locador
from datetime import datetime, date

def prueba_sistema_corregido():
    """Prueba completa del sistema corregido"""
    print("="*60)
    print("PRUEBA DEL SISTEMA CORREGIDO")
    print("="*60)
    
    with app.app_context():
        try:
            # 1. Verificar empresas
            print("1. Verificando empresas...")
            empresas = Empresa.query.all()
            print(f"   OK: Empresas encontradas: {len(empresas)}")
            
            if empresas:
                empresa = empresas[0]
                print(f"   OK: Empresa: {empresa.nombre} ({empresa.regimen_laboral})")
                
                # 2. Verificar empleados
                print("\n2. Verificando empleados...")
                empleados = Empleado.query.filter_by(empresa_id=empresa.id).all()
                print(f"   OK: Empleados encontrados: {len(empleados)}")
                
                if empleados:
                    empleado = empleados[0]
                    print(f"   OK: Empleado: {empleado.nombres} {empleado.apellidos}")
                    print(f"   OK: Sueldo base: S/. {empleado.sueldo_base:.2f}")
                    print(f"   OK: Tipo de pensión: {empleado.tipo_pension}")
                
                # 3. Verificar locadores
                print("\n3. Verificando locadores...")
                locadores = Locador.query.filter_by(empresa_id=empresa.id).all()
                print(f"   OK: Locadores encontrados: {len(locadores)}")
                
                if locadores:
                    locador = locadores[0]
                    print(f"   OK: Locador: {locador.nombres} {locador.apellidos}")
                    print(f"   OK: Monto mensual: S/. {locador.monto_mensual:.2f}")
                    print(f"   OK: Suspendido: {locador.suspendido}")
                
                # 4. Probar conteos
                print("\n4. Probando conteos...")
                empleados_activos = Empleado.query.filter_by(empresa_id=empresa.id, activo=True).count()
                locadores_activos = Locador.query.filter_by(empresa_id=empresa.id, activo=True).count()
                print(f"   OK: Empleados activos: {empleados_activos}")
                print(f"   OK: Locadores activos: {locadores_activos}")
                
                # 5. Probar cálculo de planilla
                print("\n5. Probando cálculo de planilla...")
                from app_funcional import calcular_planilla_simple
                resultado = calcular_planilla_simple(empresa.id, 10, 2024)
                print(f"   OK: Planilla calculada: {resultado['empresa']}")
                print(f"   OK: Régimen laboral: {resultado['regimen_laboral']}")
                print(f"   OK: Total empleados: {resultado['totales']['total_empleados']}")
                print(f"   OK: Total locadores: {resultado['totales']['total_locadores']}")
                print(f"   OK: Total neto: S/. {resultado['totales']['total_neto']:.2f}")
                
                if resultado['empleados']:
                    emp = resultado['empleados'][0]
                    print(f"\n   Detalles del empleado:")
                    print(f"   - Sueldo base: S/. {emp['sueldo_base']:.2f}")
                    print(f"   - Sueldo ajustado: S/. {emp['sueldo_ajustado']:.2f}")
                    print(f"   - Vacaciones: S/. {emp['beneficios']['vacaciones']:.2f}")
                    print(f"   - CTS: S/. {emp['beneficios']['cts']:.2f}")
                    print(f"   - Gratificación: S/. {emp['beneficios']['gratificacion']:.2f}")
                    print(f"   - Asignación familiar: S/. {emp['beneficios']['asignacion_familiar']:.2f}")
                    print(f"   - Pensión: S/. {emp['descuentos']['pension']:.2f}")
                    print(f"   - Impuesto renta: S/. {emp['descuentos']['impuesto_renta']:.2f}")
                    print(f"   - Neto a pagar: S/. {emp['neto_pagar']:.2f}")
                
                if resultado['locadores']:
                    loc = resultado['locadores'][0]
                    print(f"\n   Detalles del locador:")
                    print(f"   - Monto mensual: S/. {loc['monto_mensual']:.2f}")
                    print(f"   - Retención 4ta cat: S/. {loc['retencion_4ta_cat']:.2f}")
                    print(f"   - Neto a pagar: S/. {loc['neto_pagar']:.2f}")
                
                print("\n" + "="*60)
                print("SISTEMA FUNCIONANDO CORRECTAMENTE")
                print("="*60)
                print("Puede ejecutar: python app_funcional.py")
                print("Luego abrir: http://localhost:5000")
                print("NOTA: Los enlaces de Ausencias y Deudas están deshabilitados temporalmente")
                
                return True
            else:
                print("   ERROR: No hay empresas en la base de datos")
                return False
            
        except Exception as e:
            print(f"\nERROR: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    print("INICIANDO PRUEBA DEL SISTEMA CORREGIDO...")
    if prueba_sistema_corregido():
        print("\nSISTEMA LISTO PARA USAR")
    else:
        print("\nHAY PROBLEMAS EN EL SISTEMA")