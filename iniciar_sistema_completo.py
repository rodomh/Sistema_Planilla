#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Iniciar sistema completo con base de datos inicializada
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_completo import app, db, Empresa, Empleado, Locador
from datetime import date

def iniciar_sistema_completo():
    """Iniciar sistema completo con datos de ejemplo"""
    print("INICIANDO SISTEMA COMPLETO...")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Crear todas las tablas
            db.create_all()
            print("✓ Base de datos creada con SQLAlchemy")
            
            # Verificar si ya hay datos
            if Empresa.query.count() == 0:
                print("📊 Creando datos de ejemplo...")
                
                # Crear empresas
                empresas_data = [
                    {
                        'nombre': 'Inversiones IH SRL',
                        'ruc': '20123456789',
                        'regimen_laboral': 'microempresa',
                        'direccion': 'Av. Principal 123, Lima',
                        'telefono': '987654321',
                        'email': 'info@inversionesih.com'
                    },
                    {
                        'nombre': 'Servicios Generales SAC',
                        'ruc': '20234567890',
                        'regimen_laboral': 'pequeña_empresa',
                        'direccion': 'Jr. Comercio 456, Lima',
                        'telefono': '987654322',
                        'email': 'info@serviciosgenerales.com'
                    },
                    {
                        'nombre': 'Corporación Empresarial S.A.C.',
                        'ruc': '20345678901',
                        'regimen_laboral': 'general',
                        'direccion': 'Av. Industrial 789, Lima',
                        'telefono': '987654323',
                        'email': 'info@corporacionempresarial.com'
                    }
                ]
                
                for emp_data in empresas_data:
                    empresa = Empresa(**emp_data)
                    db.session.add(empresa)
                
                db.session.commit()
                print("✓ 3 empresas creadas")
                
                # Crear empleados
                empleados_data = [
                    # Microempresa
                    {
                        'empresa_id': 1,
                        'nombres': 'Juan Carlos',
                        'apellidos': 'Pérez García',
                        'dni': '12345678',
                        'sueldo_base': 1500.0,
                        'fecha_ingreso': date(2024, 1, 15),
                        'fecha_nacimiento': date(1990, 5, 20),
                        'direccion': 'Av. Lima 123',
                        'telefono': '987654321',
                        'email': 'juan@email.com',
                        'tipo_pension': 'ONP',
                        'tipo_pago': 'mensual',
                        'cuenta_bancaria': '1234567890123456',
                        'banco': 'BCP',
                        'descuento_alimentos': 0.0
                    },
                    {
                        'empresa_id': 1,
                        'nombres': 'María Elena',
                        'apellidos': 'López Silva',
                        'dni': '87654321',
                        'sueldo_base': 2000.0,
                        'fecha_ingreso': date(2024, 2, 1),
                        'fecha_nacimiento': date(1985, 8, 15),
                        'direccion': 'Jr. Paz 456',
                        'telefono': '987654322',
                        'email': 'maria@email.com',
                        'tipo_pension': 'AFP',
                        'afp_codigo': 'PRIMA',
                        'tipo_pago': 'quincenal',
                        'cuenta_bancaria': '9876543210987654',
                        'banco': 'BBVA',
                        'descuento_alimentos': 200.0
                    },
                    # Pequeña Empresa
                    {
                        'empresa_id': 2,
                        'nombres': 'Carlos',
                        'apellidos': 'Mendoza Vega',
                        'dni': '11223344',
                        'sueldo_base': 1800.0,
                        'fecha_ingreso': date(2024, 3, 10),
                        'fecha_nacimiento': date(1988, 12, 10),
                        'direccion': 'Av. Comercio 789',
                        'telefono': '987654323',
                        'email': 'carlos@email.com',
                        'tipo_pension': 'ONP',
                        'tipo_pago': 'mensual',
                        'cuenta_bancaria': '1122334455667788',
                        'banco': 'SCOTIABANK',
                        'descuento_alimentos': 150.0
                    },
                    # Régimen General
                    {
                        'empresa_id': 3,
                        'nombres': 'Ana María',
                        'apellidos': 'Rodríguez Castro',
                        'dni': '55667788',
                        'sueldo_base': 2500.0,
                        'fecha_ingreso': date(2024, 1, 20),
                        'fecha_nacimiento': date(1982, 3, 25),
                        'direccion': 'Av. Industrial 321',
                        'telefono': '987654324',
                        'email': 'ana@email.com',
                        'tipo_pension': 'AFP',
                        'afp_codigo': 'PROFUTURO',
                        'tipo_pago': 'mensual',
                        'cuenta_bancaria': '5566778899001122',
                        'banco': 'INTERBANK',
                        'descuento_alimentos': 300.0
                    }
                ]
                
                for emp_data in empleados_data:
                    empleado = Empleado(**emp_data)
                    db.session.add(empleado)
                
                db.session.commit()
                print("✓ 4 empleados creados")
                
                # Crear locadores
                locadores_data = [
                    {
                        'empresa_id': 1,
                        'nombres': 'Luis',
                        'apellidos': 'Herrera Morales',
                        'dni': '99887766',
                        'monto_mensual': 3000.0,
                        'fecha_inicio': date(2024, 2, 15),
                        'suspendido': False,
                        'cuenta_bancaria': '9988776655443322',
                        'banco': 'BCP',
                        'descuento_alimentos': 250.0
                    },
                    {
                        'empresa_id': 2,
                        'nombres': 'Elena',
                        'apellidos': 'Díaz Paz',
                        'dni': '44332211',
                        'monto_mensual': 2800.0,
                        'fecha_inicio': date(2024, 3, 5),
                        'suspendido': False,
                        'cuenta_bancaria': '4433221100998877',
                        'banco': 'BBVA',
                        'descuento_alimentos': 0.0
                    },
                    {
                        'empresa_id': 3,
                        'nombres': 'Roberto',
                        'apellidos': 'Sánchez Torres',
                        'dni': '77889900',
                        'monto_mensual': 4000.0,
                        'fecha_inicio': date(2024, 1, 10),
                        'suspendido': True,
                        'cuenta_bancaria': '7788990011223344',
                        'banco': 'SCOTIABANK',
                        'descuento_alimentos': 400.0
                    }
                ]
                
                for loc_data in locadores_data:
                    locador = Locador(**loc_data)
                    db.session.add(locador)
                
                db.session.commit()
                print("✓ 3 locadores creados")
            else:
                print("✓ Datos ya existen en la base de datos")
            
            # Verificar datos
            empresas = Empresa.query.all()
            empleados = Empleado.query.filter_by(activo=True).all()
            locadores = Locador.query.filter_by(activo=True).all()
            
            print(f"\n📊 DATOS VERIFICADOS:")
            print(f"   ✓ Empresas: {len(empresas)}")
            print(f"   ✓ Empleados activos: {len(empleados)}")
            print(f"   ✓ Locadores activos: {len(locadores)}")
            
            print("\n" + "=" * 50)
            print("✅ SISTEMA COMPLETO INICIALIZADO EXITOSAMENTE")
            print("=" * 50)
            print("🌐 Iniciando servidor en: http://localhost:5000")
            print("📊 Funcionalidades disponibles:")
            print("   ✓ Gestión de empresas (3 regímenes)")
            print("   ✓ Gestión de empleados y locadores")
            print("   ✓ Tipos de pago (mensual/quincenal)")
            print("   ✓ Descuentos por alimentos")
            print("   ✓ Información bancaria")
            print("   ✓ Cálculo de planillas por régimen")
            print("   ✓ Exportación a Excel")
            print("   ✓ Edición y eliminación de personal")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al inicializar sistema: {str(e)}")
            return False

if __name__ == "__main__":
    if iniciar_sistema_completo():
        print("\n🚀 Iniciando servidor Flask...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ No se pudo inicializar el sistema")
