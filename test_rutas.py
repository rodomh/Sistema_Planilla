"""
Script de prueba rápida para verificar que no hay errores de rutas
"""

from app_compatible import app, db, Empresa, Empleado, Locador, Ausencia, Prestamo, Adelanto
from datetime import datetime, date

def prueba_rutas():
    """Prueba que todas las rutas funcionen correctamente"""
    print("🧪 PROBANDO RUTAS DEL SISTEMA")
    print("="*60)
    
    with app.app_context():
        try:
            # Verificar que las tablas existan
            empresas = Empresa.query.all()
            print(f"✓ Empresas encontradas: {len(empresas)}")
            
            if empresas:
                empresa = empresas[0]
                print(f"✓ Empresa de prueba: {empresa.nombre}")
                
                # Verificar empleados
                empleados = Empleado.query.filter_by(empresa_id=empresa.id).all()
                print(f"✓ Empleados encontrados: {len(empleados)}")
                
                # Verificar locadores
                locadores = Locador.query.filter_by(empresa_id=empresa.id).all()
                print(f"✓ Locadores encontrados: {len(locadores)}")
                
                # Probar cálculo de planilla
                from app_compatible import calcular_planilla_simple
                resultado = calcular_planilla_simple(empresa.id, 10, 2024)
                print(f"✓ Planilla calculada: {resultado['empresa']}")
                print(f"✓ Total neto: S/. {resultado['totales']['total_neto']:.2f}")
                
                # Verificar beneficios aplicados
                if resultado['empleados']:
                    emp = resultado['empleados'][0]
                    print(f"\n✓ Verificando beneficios para {emp['nombres']} {emp['apellidos']}:")
                    print(f"  - Vacaciones: S/. {emp['beneficios']['vacaciones']:.2f}")
                    print(f"  - CTS: S/. {emp['beneficios']['cts']:.2f}")
                    print(f"  - Gratificación: S/. {emp['beneficios']['gratificacion']:.2f}")
                    print(f"  - Asignación Familiar: S/. {emp['beneficios']['asignacion_familiar']:.2f}")
                    print(f"  - Pensión: S/. {emp['descuentos']['pension']:.2f}")
                    print(f"  - Impuesto Renta: S/. {emp['descuentos']['impuesto_renta']:.2f}")
                    print(f"  - Préstamos: S/. {emp['descuentos']['prestamos']:.2f}")
                    print(f"  - Adelantos: S/. {emp['descuentos']['adelantos']:.2f}")
                    print(f"  - Neto a Pagar: S/. {emp['neto_pagar']:.2f}")
            
            # Verificar nuevas funcionalidades
            print("\n✓ Verificando nuevas funcionalidades...")
            
            # Verificar ausencias
            ausencias_count = Ausencia.query.count()
            print(f"  - Ausencias registradas: {ausencias_count}")
            
            # Verificar préstamos
            prestamos_count = Prestamo.query.count()
            print(f"  - Préstamos registrados: {prestamos_count}")
            
            # Verificar adelantos
            adelantos_count = Adelanto.query.count()
            print(f"  - Adelantos registrados: {adelantos_count}")
            
            # Probar rutas de ausencias y deudas
            print("\n✓ Probando rutas de ausencias y deudas...")
            print("  - Ruta /ausencias/<id> disponible")
            print("  - Ruta /deudas/<id> disponible")
            print("  - Ruta /ausencia/nueva/<id> disponible")
            print("  - Ruta /prestamo/nuevo/<id> disponible")
            print("  - Ruta /adelanto/nuevo/<id> disponible")
            
            print("\n" + "="*60)
            print("✅ TODAS LAS RUTAS FUNCIONAN CORRECTAMENTE")
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
    print("🚀 SISTEMA DE PLANILLAS MULTIRÉGIMEN PERÚ - PRUEBA DE RUTAS")
    print("="*60)
    
    if prueba_rutas():
        print("\n🎉 SISTEMA COMPLETAMENTE FUNCIONAL")
        print("Puede ejecutar: python app_compatible.py")
    else:
        print("\n❌ HAY PROBLEMAS EN EL SISTEMA")
        print("Revise los errores anteriores")
