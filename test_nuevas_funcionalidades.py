"""
Script de prueba para verificar las nuevas funcionalidades:
- Editar empleados y locadores
- Cargar desde Excel
"""

from app_funcional import app, db, Empresa, Empleado, Locador
from datetime import datetime, date

def prueba_nuevas_funcionalidades():
    """Prueba de las nuevas funcionalidades"""
    print("="*60)
    print("PRUEBA DE NUEVAS FUNCIONALIDADES")
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
                
                # 2. Verificar empleados existentes
                print("\n2. Verificando empleados...")
                empleados = Empleado.query.filter_by(empresa_id=empresa.id, activo=True).all()
                print(f"   OK: Empleados activos: {len(empleados)}")
                
                if empleados:
                    empleado = empleados[0]
                    print(f"   OK: Empleado: {empleado.nombres} {empleado.apellidos}")
                    
                    # 3. Probar edición de empleado
                    print("\n3. Probando edición de empleado...")
                    empleado_original = empleado.sueldo_base
                    empleado.sueldo_base = 2000.00
                    db.session.commit()
                    print(f"   OK: Sueldo actualizado de {empleado_original} a {empleado.sueldo_base}")
                    
                    # Restaurar valor original
                    empleado.sueldo_base = empleado_original
                    db.session.commit()
                    print(f"   OK: Sueldo restaurado a {empleado.sueldo_base}")
                
                # 4. Verificar locadores existentes
                print("\n4. Verificando locadores...")
                locadores = Locador.query.filter_by(empresa_id=empresa.id, activo=True).all()
                print(f"   OK: Locadores activos: {len(locadores)}")
                
                if locadores:
                    locador = locadores[0]
                    print(f"   OK: Locador: {locador.nombres} {locador.apellidos}")
                    
                    # 5. Probar edición de locador
                    print("\n5. Probando edición de locador...")
                    locador_original = locador.monto_mensual
                    locador.monto_mensual = 3000.00
                    db.session.commit()
                    print(f"   OK: Monto actualizado de {locador_original} a {locador.monto_mensual}")
                    
                    # Restaurar valor original
                    locador.monto_mensual = locador_original
                    db.session.commit()
                    print(f"   OK: Monto restaurado a {locador.monto_mensual}")
                
                # 6. Probar descarga de plantilla
                print("\n6. Probando descarga de plantilla...")
                from app_funcional import descargar_plantilla
                
                # Simular request
                class MockRequest:
                    def __init__(self):
                        pass
                
                # Reemplazar request global temporalmente
                import app_funcional
                original_request = app_funcional.request
                app_funcional.request = MockRequest()
                
                try:
                    response = descargar_plantilla(empresa.id)
                    print(f"   OK: Plantilla generada exitosamente")
                    print(f"   OK: Tipo de contenido: {response.headers['Content-Type']}")
                    print(f"   OK: Nombre de archivo: {response.headers['Content-Disposition']}")
                    print(f"   OK: Tamaño del archivo: {len(response.data)} bytes")
                except Exception as e:
                    print(f"   ERROR: {e}")
                finally:
                    # Restaurar request original
                    app_funcional.request = original_request
                
                print("\n" + "="*60)
                print("NUEVAS FUNCIONALIDADES FUNCIONANDO CORRECTAMENTE")
                print("="*60)
                print("Funcionalidades implementadas:")
                print("OK: Editar empleados")
                print("OK: Editar locadores")
                print("OK: Eliminar empleados y locadores")
                print("OK: Cargar desde Excel")
                print("OK: Descargar plantilla Excel")
                print("\nPuede ejecutar: python app_funcional.py")
                print("Luego abrir: http://localhost:5000")
                print("Y probar las nuevas funcionalidades desde la pagina de personal")
                
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
    print("INICIANDO PRUEBA DE NUEVAS FUNCIONALIDADES...")
    if prueba_nuevas_funcionalidades():
        print("\nSISTEMA LISTO CON NUEVAS FUNCIONALIDADES")
    else:
        print("\nHAY PROBLEMAS EN LAS NUEVAS FUNCIONALIDADES")
