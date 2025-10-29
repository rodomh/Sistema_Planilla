"""
Script de prueba para verificar que el sistema funcione correctamente
"""

from app_compatible import app, db, Empresa, Empleado, Locador
from datetime import datetime, date

def prueba_sistema_completo():
    """Prueba completa del sistema"""
    print("="*60)
    print("PRUEBA COMPLETA DEL SISTEMA")
    print("="*60)
    
    with app.app_context():
        try:
            # 1. Verificar empresas
            print("1. Verificando empresas...")
            empresas = Empresa.query.all()
            print(f"   OK: Empresas encontradas: {len(empresas)}")
            
            if not empresas:
                print("   ERROR: No hay empresas. Creando empresa de prueba...")
                empresa = Empresa(
                    nombre='Empresa de Prueba S.A.C.',
                    ruc='20123456789',
                    regimen_laboral='general',
                    direccion='Av. Principal 123, Lima',
                    telefono='01-2345678',
                    email='info@empresa-prueba.com'
                )
                db.session.add(empresa)
                db.session.commit()
                print("   OK: Empresa de prueba creada")
                empresas = [empresa]
            
            empresa = empresas[0]
            print(f"   OK: Empresa: {empresa.nombre} ({empresa.regimen_laboral})")
            
            # 2. Verificar empleados
            print("\n2. Verificando empleados...")
            empleados = Empleado.query.filter_by(empresa_id=empresa.id).all()
            print(f"   OK: Empleados encontrados: {len(empleados)}")
            
            if not empleados:
                print("   ERROR: No hay empleados. Creando empleado de prueba...")
                empleado = Empleado(
                    empresa_id=empresa.id,
                    nombres='Juan Carlos',
                    apellidos='Pérez García',
                    dni='12345678',
                    sueldo_base=1500.00,
                    fecha_ingreso=date(2024, 1, 15),
                    tipo_pension='ONP',
                    cuenta_bancaria='1234567890123456',
                    banco='BCP',
                    tipo_pago='mensual',
                    activo=True
                )
                db.session.add(empleado)
                db.session.commit()
                print("   OK: Empleado de prueba creado")
                empleados = [empleado]
            
            empleado = empleados[0]
            print(f"   OK: Empleado: {empleado.nombres} {empleado.apellidos}")
            print(f"   OK: Cuenta bancaria: {empleado.cuenta_bancaria}")
            print(f"   OK: Banco: {empleado.banco}")
            print(f"   OK: Tipo de pago: {empleado.tipo_pago}")
            
            # 3. Verificar locadores
            print("\n3. Verificando locadores...")
            locadores = Locador.query.filter_by(empresa_id=empresa.id).all()
            print(f"   OK: Locadores encontrados: {len(locadores)}")
            
            if not locadores:
                print("   ERROR: No hay locadores. Creando locador de prueba...")
                locador = Locador(
                    empresa_id=empresa.id,
                    nombres='María Elena',
                    apellidos='Rodríguez López',
                    dni='87654321',
                    monto_mensual=2000.00,
                    fecha_inicio=date(2024, 2, 1),
                    cuenta_bancaria='9876543210987654',
                    banco='BBVA',
                    suspendido=False,
                    activo=True
                )
                db.session.add(locador)
                db.session.commit()
                print("   OK: Locador de prueba creado")
                locadores = [locador]
            
            locador = locadores[0]
            print(f"   OK: Locador: {locador.nombres} {locador.apellidos}")
            print(f"   OK: Cuenta bancaria: {locador.cuenta_bancaria}")
            print(f"   OK: Banco: {locador.banco}")
            
            # 4. Probar conteos
            print("\n4. Probando conteos...")
            empleados_activos = Empleado.query.filter_by(empresa_id=empresa.id, activo=True).count()
            locadores_activos = Locador.query.filter_by(empresa_id=empresa.id, activo=True).count()
            print(f"   OK: Empleados activos: {empleados_activos}")
            print(f"   OK: Locadores activos: {locadores_activos}")
            
            # 5. Probar cálculo de planilla
            print("\n5. Probando cálculo de planilla...")
            from app_compatible import calcular_planilla_simple
            resultado = calcular_planilla_simple(empresa.id, 10, 2024)
            print(f"   OK: Planilla calculada: {resultado['empresa']}")
            print(f"   OK: Total empleados: {resultado['totales']['total_empleados']}")
            print(f"   OK: Total locadores: {resultado['totales']['total_locadores']}")
            print(f"   OK: Total neto: S/. {resultado['totales']['total_neto']:.2f}")
            
            if resultado['empleados']:
                emp = resultado['empleados'][0]
                print(f"\n   Detalles del empleado:")
                print(f"   - Sueldo base: S/. {emp['sueldo_base']:.2f}")
                print(f"   - Sueldo ajustado: S/. {emp['sueldo_ajustado']:.2f}")
                print(f"   - Tipo de pago: {emp['tipo_pago']}")
                print(f"   - Cuenta bancaria: {emp['cuenta_bancaria']}")
                print(f"   - Banco: {emp['banco']}")
                print(f"   - Días trabajados: {emp['dias_trabajados']}")
                print(f"   - Neto a pagar: S/. {emp['neto_pagar']:.2f}")
            
            print("\n" + "="*60)
            print("SISTEMA FUNCIONANDO CORRECTAMENTE")
            print("="*60)
            print("Puede ejecutar: python app_compatible.py")
            print("Luego abrir: http://localhost:5000")
            
            return True
            
        except Exception as e:
            print(f"\nERROR: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    print("INICIANDO PRUEBA DEL SISTEMA...")
    if prueba_sistema_completo():
        print("\nSISTEMA LISTO PARA USAR")
    else:
        print("\nHAY PROBLEMAS EN EL SISTEMA")
