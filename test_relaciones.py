"""
Script de prueba específico para verificar las relaciones de los modelos
"""

from app_compatible import app, db, Empresa, Empleado, Locador, Ausencia, Prestamo, Adelanto
from datetime import datetime, date

def prueba_relaciones():
    """Prueba que todas las relaciones de los modelos funcionen correctamente"""
    print("🧪 PROBANDO RELACIONES DE LOS MODELOS")
    print("="*60)
    
    with app.app_context():
        try:
            # 1. Verificar empresas
            print("1. Verificando empresas...")
            empresas = Empresa.query.all()
            print(f"   ✓ Empresas encontradas: {len(empresas)}")
            
            if not empresas:
                print("   ❌ No hay empresas. Ejecute init_sqlite_directo.py primero")
                return False
            
            empresa = empresas[0]
            print(f"   ✓ Empresa de prueba: {empresa.nombre}")
            
            # 2. Verificar empleados
            print("\n2. Verificando empleados...")
            empleados = Empleado.query.filter_by(empresa_id=empresa.id).all()
            print(f"   ✓ Empleados encontrados: {len(empleados)}")
            
            if not empleados:
                print("   ❌ No hay empleados. Agregue empleados desde la interfaz web")
                return False
            
            empleado = empleados[0]
            print(f"   ✓ Empleado de prueba: {empleado.nombres} {empleado.apellidos}")
            
            # 3. Probar relaciones de ausencias
            print("\n3. Probando relaciones de ausencias...")
            try:
                # Crear una ausencia de prueba
                ausencia = Ausencia(
                    empleado_id=empleado.id,
                    fecha=date.today(),
                    tipo='falta',
                    justificada=False,
                    motivo='Prueba de relación',
                    horas_perdidas=8.0
                )
                db.session.add(ausencia)
                db.session.commit()
                print("   ✓ Ausencia creada exitosamente")
                
                # Verificar relación
                ausencia_creada = Ausencia.query.filter_by(empleado_id=empleado.id).first()
                if ausencia_creada and ausencia_creada.empleado:
                    print(f"   ✓ Relación empleado funcionando: {ausencia_creada.empleado.nombres}")
                else:
                    print("   ❌ Error en relación empleado")
                    return False
                
                # Limpiar prueba
                db.session.delete(ausencia_creada)
                db.session.commit()
                print("   ✓ Ausencia de prueba eliminada")
                
            except Exception as e:
                print(f"   ❌ Error probando ausencias: {e}")
                return False
            
            # 4. Probar relaciones de préstamos
            print("\n4. Probando relaciones de préstamos...")
            try:
                # Crear un préstamo de prueba
                prestamo = Prestamo(
                    empleado_id=empleado.id,
                    monto_total=1000.0,
                    monto_pendiente=1000.0,
                    cuota_mensual=100.0,
                    fecha_prestamo=date.today(),
                    motivo='Prueba de relación'
                )
                db.session.add(prestamo)
                db.session.commit()
                print("   ✓ Préstamo creado exitosamente")
                
                # Verificar relación
                prestamo_creado = Prestamo.query.filter_by(empleado_id=empleado.id).first()
                if prestamo_creado and prestamo_creado.empleado:
                    print(f"   ✓ Relación empleado funcionando: {prestamo_creado.empleado.nombres}")
                else:
                    print("   ❌ Error en relación empleado")
                    return False
                
                # Limpiar prueba
                db.session.delete(prestamo_creado)
                db.session.commit()
                print("   ✓ Préstamo de prueba eliminado")
                
            except Exception as e:
                print(f"   ❌ Error probando préstamos: {e}")
                return False
            
            # 5. Probar relaciones de adelantos
            print("\n5. Probando relaciones de adelantos...")
            try:
                # Crear un adelanto de prueba
                adelanto = Adelanto(
                    empleado_id=empleado.id,
                    monto=500.0,
                    fecha_adelanto=date.today(),
                    mes_aplicar=10,
                    año_aplicar=2024,
                    motivo='Prueba de relación'
                )
                db.session.add(adelanto)
                db.session.commit()
                print("   ✓ Adelanto creado exitosamente")
                
                # Verificar relación
                adelanto_creado = Adelanto.query.filter_by(empleado_id=empleado.id).first()
                if adelanto_creado and adelanto_creado.empleado:
                    print(f"   ✓ Relación empleado funcionando: {adelanto_creado.empleado.nombres}")
                else:
                    print("   ❌ Error en relación empleado")
                    return False
                
                # Limpiar prueba
                db.session.delete(adelanto_creado)
                db.session.commit()
                print("   ✓ Adelanto de prueba eliminado")
                
            except Exception as e:
                print(f"   ❌ Error probando adelantos: {e}")
                return False
            
            # 6. Probar cálculo de planilla con relaciones
            print("\n6. Probando cálculo de planilla con relaciones...")
            try:
                from app_compatible import calcular_planilla_simple
                resultado = calcular_planilla_simple(empresa.id, 10, 2024)
                print(f"   ✓ Planilla calculada: {resultado['empresa']}")
                print(f"   ✓ Total neto: S/. {resultado['totales']['total_neto']:.2f}")
                
                if resultado['empleados']:
                    emp = resultado['empleados'][0]
                    print(f"   ✓ Empleado: {emp['nombres']} {emp['apellidos']}")
                    print(f"   ✓ Días trabajados: {emp['dias_trabajados']}")
                    print(f"   ✓ Días faltados: {emp['dias_faltados']}")
                    print(f"   ✓ Neto a pagar: S/. {emp['neto_pagar']:.2f}")
                
            except Exception as e:
                print(f"   ❌ Error calculando planilla: {e}")
                return False
            
            print("\n" + "="*60)
            print("✅ TODAS LAS RELACIONES FUNCIONAN CORRECTAMENTE")
            print("="*60)
            print("El sistema está listo para usar.")
            print("Puede acceder a la interfaz web en: http://localhost:5000")
            
            return True
            
        except Exception as e:
            print(f"\n❌ ERROR DURANTE LA PRUEBA: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    print("🚀 SISTEMA DE PLANILLAS MULTIRÉGIMEN PERÚ - PRUEBA DE RELACIONES")
    print("="*60)
    
    if prueba_relaciones():
        print("\n🎉 SISTEMA COMPLETAMENTE FUNCIONAL")
        print("Puede ejecutar: python app_compatible.py")
    else:
        print("\n❌ HAY PROBLEMAS EN EL SISTEMA")
        print("Revise los errores anteriores")
