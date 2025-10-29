"""
Script para crear datos de prueba y verificar el sistema
"""

from app_temporal import app, db, Empresa, Empleado, Locador
from datetime import datetime, date

def crear_datos_prueba():
    """Crear datos de prueba para verificar el sistema"""
    print("="*60)
    print("CREANDO DATOS DE PRUEBA")
    print("="*60)
    
    with app.app_context():
        try:
            # 1. Crear empresa de prueba
            print("1. Creando empresa de prueba...")
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
            print(f"   OK: Empresa creada: {empresa.nombre}")
            
            # 2. Crear empleado de prueba
            print("\n2. Creando empleado de prueba...")
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
            print(f"   OK: Empleado creado: {empleado.nombres} {empleado.apellidos}")
            print(f"   OK: Cuenta bancaria: {empleado.cuenta_bancaria}")
            print(f"   OK: Banco: {empleado.banco}")
            print(f"   OK: Tipo de pago: {empleado.tipo_pago}")
            
            # 3. Crear locador de prueba
            print("\n3. Creando locador de prueba...")
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
            print(f"   OK: Locador creado: {locador.nombres} {locador.apellidos}")
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
            from app_temporal import calcular_planilla_simple
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
                print(f"   - Neto a pagar: S/. {emp['neto_pagar']:.2f}")
            
            print("\n" + "="*60)
            print("DATOS DE PRUEBA CREADOS EXITOSAMENTE")
            print("="*60)
            print("Sistema listo para usar en: http://localhost:5000")
            
            return True
            
        except Exception as e:
            print(f"\nERROR: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    print("INICIANDO CREACIÓN DE DATOS DE PRUEBA...")
    if crear_datos_prueba():
        print("\nSISTEMA LISTO PARA USAR")
    else:
        print("\nHAY PROBLEMAS EN EL SISTEMA")
