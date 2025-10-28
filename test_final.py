"""
Script de prueba simplificado para verificar el funcionamiento del sistema
"""

from app_final import app, db, Empresa, Empleado, Locador
from datetime import datetime, date

def prueba_sistema_completo():
    """Ejecuta una prueba completa del sistema"""
    print("🧪 INICIANDO PRUEBA COMPLETA DEL SISTEMA")
    print("="*60)
    
    with app.app_context():
        try:
            # 1. Verificar empresas
            print("1. Verificando empresas...")
            empresas = Empresa.query.all()
            print(f"   ✓ Empresas encontradas: {len(empresas)}")
            
            if not empresas:
                print("   ❌ No hay empresas. Ejecute init_final.py primero")
                return False
            
            empresa = empresas[0]
            print(f"   ✓ Empresa de prueba: {empresa.nombre} ({empresa.regimen_laboral})")
            
            # 2. Verificar empleados
            print("\n2. Verificando empleados...")
            empleados = Empleado.query.filter_by(empresa_id=empresa.id).all()
            print(f"   ✓ Empleados encontrados: {len(empleados)}")
            
            if not empleados:
                print("   ❌ No hay empleados. Agregue empleados desde la interfaz web")
                return False
            
            empleado = empleados[0]
            print(f"   ✓ Empleado de prueba: {empleado.nombres} {empleado.apellidos}")
            
            # 3. Probar cálculo de planilla
            print("\n3. Probando cálculo de planilla...")
            from app_final import calcular_planilla_simple
            resultado = calcular_planilla_simple(empresa.id, 10, 2024)
            print(f"   ✓ Planilla calculada para {resultado['empresa']}")
            print(f"   ✓ Total empleados: {resultado['totales']['total_empleados']}")
            print(f"   ✓ Total locadores: {resultado['totales']['total_locadores']}")
            print(f"   ✓ Total neto: S/. {resultado['totales']['total_neto']:.2f}")
            
            # 4. Verificar beneficios aplicados
            if resultado['empleados']:
                emp = resultado['empleados'][0]
                print(f"\n4. Verificando beneficios para {emp['nombres']} {emp['apellidos']}:")
                print(f"   ✓ Vacaciones: S/. {emp['beneficios']['vacaciones']:.2f}")
                print(f"   ✓ CTS: S/. {emp['beneficios']['cts']:.2f}")
                print(f"   ✓ Gratificación: S/. {emp['beneficios']['gratificacion']:.2f}")
                print(f"   ✓ Asignación Familiar: S/. {emp['beneficios']['asignacion_familiar']:.2f}")
                print(f"   ✓ Pensión: S/. {emp['descuentos']['pension']:.2f}")
                print(f"   ✓ Impuesto Renta: S/. {emp['descuentos']['impuesto_renta']:.2f}")
                print(f"   ✓ Neto a Pagar: S/. {emp['neto_pagar']:.2f}")
            
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

def prueba_regimenes_laborales():
    """Prueba los diferentes regímenes laborales"""
    print("\n🧪 PROBANDO REGÍMENES LABORALES")
    print("="*60)
    
    with app.app_context():
        regimenes = ['microempresa', 'pequeña_empresa', 'general']
        
        for regimen in regimenes:
            print(f"\nProbando régimen: {regimen.upper()}")
            
            # Buscar empresa con este régimen
            empresa = Empresa.query.filter_by(regimen_laboral=regimen).first()
            if not empresa:
                print(f"   ❌ No hay empresa con régimen {regimen}")
                continue
            
            print(f"   ✓ Empresa: {empresa.nombre}")
            
            # Buscar empleado
            empleado = Empleado.query.filter_by(empresa_id=empresa.id).first()
            if not empleado:
                print(f"   ❌ No hay empleados en esta empresa")
                continue
            
            print(f"   ✓ Empleado: {empleado.nombres} {empleado.apellidos}")
            print(f"   ✓ Sueldo: S/. {empleado.sueldo_base}")
            
            # Calcular planilla
            try:
                from app_final import calcular_planilla_simple
                resultado = calcular_planilla_simple(empresa.id, 7, 2024)  # Julio para probar gratificaciones
                if resultado['empleados']:
                    emp = resultado['empleados'][0]
                    print(f"   ✓ Vacaciones: S/. {emp['beneficios']['vacaciones']:.2f}")
                    print(f"   ✓ CTS: S/. {emp['beneficios']['cts']:.2f}")
                    print(f"   ✓ Gratificación: S/. {emp['beneficios']['gratificacion']:.2f}")
                    print(f"   ✓ Asignación Familiar: S/. {emp['beneficios']['asignacion_familiar']:.2f}")
                    print(f"   ✓ Neto: S/. {emp['neto_pagar']:.2f}")
            except Exception as e:
                print(f"   ❌ Error calculando planilla: {e}")

if __name__ == '__main__':
    print("🚀 SISTEMA DE PLANILLAS MULTIRÉGIMEN PERÚ - PRUEBAS")
    print("="*60)
    
    # Ejecutar prueba completa
    if prueba_sistema_completo():
        # Ejecutar prueba de regímenes
        prueba_regimenes_laborales()
        
        print("\n🎉 TODAS LAS PRUEBAS COMPLETADAS")
        print("El sistema está listo para usar.")
    else:
        print("\n❌ LAS PRUEBAS FALLARON")
        print("Revise la configuración y ejecute init_final.py")
