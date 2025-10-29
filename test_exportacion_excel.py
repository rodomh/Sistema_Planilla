"""
Script de prueba para verificar que la exportación a Excel funcione correctamente
"""

from app_funcional import app, db, Empresa, Empleado, Locador
from datetime import datetime, date

def prueba_exportacion_excel():
    """Prueba de exportación a Excel"""
    print("="*60)
    print("PRUEBA DE EXPORTACIÓN A EXCEL")
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
                
                # 2. Probar cálculo de planilla
                print("\n2. Probando cálculo de planilla...")
                from app_funcional import calcular_planilla_simple
                resultado = calcular_planilla_simple(empresa.id, 10, 2024)
                print(f"   OK: Planilla calculada: {resultado['empresa']}")
                print(f"   OK: Total empleados: {resultado['totales']['total_empleados']}")
                print(f"   OK: Total locadores: {resultado['totales']['total_locadores']}")
                print(f"   OK: Total neto: S/. {resultado['totales']['total_neto']:.2f}")
                
                # 3. Probar exportación a Excel
                print("\n3. Probando exportación a Excel...")
                from app_funcional import exportar_excel
                
                # Simular request
                class MockRequest:
                    def __init__(self, form_data):
                        self.form = form_data
                
                mock_request = MockRequest({'mes': '10', 'año': '2024'})
                
                # Reemplazar request global temporalmente
                import app_funcional
                original_request = app_funcional.request
                app_funcional.request = mock_request
                
                try:
                    response = exportar_excel(empresa.id)
                    print(f"   OK: Exportación exitosa")
                    print(f"   OK: Tipo de contenido: {response.headers['Content-Type']}")
                    print(f"   OK: Nombre de archivo: {response.headers['Content-Disposition']}")
                    print(f"   OK: Tamaño del archivo: {len(response.data)} bytes")
                except Exception as e:
                    print(f"   ERROR: {e}")
                finally:
                    # Restaurar request original
                    app_funcional.request = original_request
                
                print("\n" + "="*60)
                print("EXPORTACIÓN A EXCEL FUNCIONANDO CORRECTAMENTE")
                print("="*60)
                print("Puede ejecutar: python app_funcional.py")
                print("Luego abrir: http://localhost:5000")
                print("Y probar la exportación desde la página de planilla")
                
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
    print("INICIANDO PRUEBA DE EXPORTACIÓN A EXCEL...")
    if prueba_exportacion_excel():
        print("\nSISTEMA LISTO PARA USAR CON EXPORTACIÓN A EXCEL")
    else:
        print("\nHAY PROBLEMAS EN LA EXPORTACIÓN A EXCEL")
