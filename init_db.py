"""
Script de inicialización del Sistema de Planillas Multirégimen Perú
Crea la base de datos y configura datos iniciales
"""

from app import app, db
from models import *
from calculadora_planilla import obtener_configuracion
from decimal import Decimal

def inicializar_base_datos():
    """Inicializa la base de datos con tablas y datos básicos"""
    print("Inicializando base de datos...")
    
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        print("✓ Tablas creadas exitosamente")
        
        # Crear configuraciones iniciales
        configuraciones_iniciales = [
            ('umbral_renta_5ta', '1025', 'Umbral mínimo no afecto para impuesto a la renta 5ta categoría'),
            ('umbral_retencion_4ta', '1500', 'Umbral para retención 4ta categoría'),
            ('tasa_retencion_4ta', '8', 'Tasa de retención 4ta categoría (%)'),
            ('asignacion_familiar', '102.50', 'Monto de asignación familiar'),
            ('tasa_pension_onp', '13', 'Tasa de pensión ONP (%)'),
            ('tasa_afp_prima', '12', 'Tasa AFP Prima (%)'),
            ('tasa_afp_integra', '12', 'Tasa AFP Integra (%)'),
            ('tasa_afp_profuturo', '12', 'Tasa AFP Profuturo (%)'),
            ('tasa_afp_habitat', '12', 'Tasa AFP Habitat (%)')
        ]
        
        for clave, valor, descripcion in configuraciones_iniciales:
            config_existente = Configuracion.query.filter_by(clave=clave).first()
            if not config_existente:
                config = Configuracion(
                    clave=clave,
                    valor=valor,
                    descripcion=descripcion
                )
                db.session.add(config)
                print(f"✓ Configuración creada: {clave} = {valor}")
        
        # Crear empresa de ejemplo
        empresa_ejemplo = Empresa.query.filter_by(ruc='20123456789').first()
        if not empresa_ejemplo:
            empresa_ejemplo = Empresa(
                nombre='Empresa de Ejemplo S.A.C.',
                ruc='20123456789',
                regimen_laboral='general',
                direccion='Av. Principal 123, Lima',
                telefono='01-2345678',
                email='info@empresa-ejemplo.com'
            )
            db.session.add(empresa_ejemplo)
            print("✓ Empresa de ejemplo creada")
        
        # Crear empleado de ejemplo
        empleado_ejemplo = Empleado.query.filter_by(dni='12345678').first()
        if not empleado_ejemplo and empresa_ejemplo:
            empleado_ejemplo = Empleado(
                empresa_id=empresa_ejemplo.id,
                nombres='Juan Carlos',
                apellidos='Pérez García',
                dni='12345678',
                sueldo_base=Decimal('1500.00'),
                fecha_ingreso=date(2024, 1, 15),
                fecha_nacimiento=date(1985, 5, 20),
                direccion='Jr. Los Olivos 456, Lima',
                telefono='987654321',
                email='juan.perez@email.com',
                tipo_pension='ONP',
                activo=True
            )
            db.session.add(empleado_ejemplo)
            print("✓ Empleado de ejemplo creado")
        
        # Crear locador de ejemplo
        locador_ejemplo = Locador.query.filter_by(dni='87654321').first()
        if not locador_ejemplo and empresa_ejemplo:
            locador_ejemplo = Locador(
                empresa_id=empresa_ejemplo.id,
                nombres='María Elena',
                apellidos='Rodríguez López',
                dni='87654321',
                monto_mensual=Decimal('2000.00'),
                fecha_inicio=date(2024, 2, 1),
                direccion='Av. Comercio 789, Lima',
                telefono='912345678',
                email='maria.rodriguez@email.com',
                suspendido=False,
                activo=True
            )
            db.session.add(locador_ejemplo)
            print("✓ Locador de ejemplo creado")
        
        # Confirmar cambios
        db.session.commit()
        print("✓ Base de datos inicializada exitosamente")

def mostrar_resumen():
    """Muestra un resumen del sistema"""
    with app.app_context():
        print("\n" + "="*60)
        print("SISTEMA DE PLANILLAS MULTIRÉGIMEN PERÚ")
        print("="*60)
        
        empresas = Empresa.query.all()
        empleados = Empleado.query.all()
        locadores = Locador.query.all()
        
        print(f"Empresas registradas: {len(empresas)}")
        for empresa in empresas:
            print(f"  - {empresa.nombre} ({empresa.regimen_laboral})")
        
        print(f"\nEmpleados registrados: {len(empleados)}")
        for empleado in empleados:
            print(f"  - {empleado.nombres} {empleado.apellidos} - S/. {empleado.sueldo_base}")
        
        print(f"\nLocadores registrados: {len(locadores)}")
        for locador in locadores:
            print(f"  - {locador.nombres} {locador.apellidos} - S/. {locador.monto_mensual}")
        
        print("\n" + "="*60)
        print("REGLAS DE NEGOCIO IMPLEMENTADAS:")
        print("="*60)
        
        reglas = {
            'microempresa': {
                'vacaciones': '15 días anuales',
                'cts': 'NO corresponde',
                'gratificaciones': 'NO corresponde',
                'asignacion_familiar': 'NO corresponde'
            },
            'pequeña_empresa': {
                'vacaciones': '15 días anuales',
                'cts': '15 días por año de servicio',
                'gratificaciones': 'Medio sueldo en Julio y Diciembre',
                'asignacion_familiar': 'S/. 102.50 (si sueldo ≤ S/. 1025)'
            },
            'general': {
                'vacaciones': '30 días anuales',
                'cts': 'Un sueldo anual',
                'gratificaciones': 'Sueldo + 9% en Julio y Diciembre',
                'asignacion_familiar': 'S/. 102.50 (si sueldo ≤ S/. 1025)'
            }
        }
        
        for regimen, beneficios in reglas.items():
            print(f"\n{regimen.upper()}:")
            for beneficio, descripcion in beneficios.items():
                print(f"  - {beneficio.title()}: {descripcion}")
        
        print("\n" + "="*60)
        print("DESCUENTOS APLICABLES:")
        print("="*60)
        print("- Pensión ONP: 13%")
        print("- Pensión AFP: 12% (según AFP)")
        print("- Impuesto a la Renta 5ta Cat.: Según tramos")
        print("- Retención 4ta Cat.: 8% (locadores, si monto > S/. 1,500)")
        
        print("\n" + "="*60)
        print("INSTRUCCIONES DE USO:")
        print("="*60)
        print("1. Ejecutar: python app.py")
        print("2. Abrir navegador en: http://localhost:5000")
        print("3. Crear empresas con diferentes regímenes laborales")
        print("4. Registrar empleados y locadores")
        print("5. Calcular planillas mensuales")
        print("6. Gestionar ausencias y deudas internas")
        
        print("\n" + "="*60)

if __name__ == '__main__':
    try:
        inicializar_base_datos()
        mostrar_resumen()
    except Exception as e:
        print(f"Error durante la inicialización: {e}")
        import traceback
        traceback.print_exc()

