#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inicializar sistema final con base de datos completa
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_completo import app, db, Empresa, Empleado, Locador, Ausencia, Prestamo, Adelanto
from datetime import date

def inicializar_sistema_final():
    """Inicializar sistema final con base de datos completa"""
    print("INICIALIZANDO SISTEMA FINAL COMPLETO...")
    print("=" * 60)
    
    with app.app_context():
        try:
            # Eliminar todas las tablas existentes
            db.drop_all()
            print("✓ Tablas existentes eliminadas")
            
            # Crear todas las tablas
            db.create_all()
            print("✓ Base de datos creada con SQLAlchemy")
            
            # Crear empresas
            print("\n📊 CREANDO EMPRESAS...")
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
            print("\n👥 CREANDO EMPLEADOS...")
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
            print("\n💼 CREANDO LOCADORES...")
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
            
            # Verificar datos
            print("\n🔍 VERIFICANDO DATOS...")
            empresas = Empresa.query.all()
            empleados = Empleado.query.filter_by(activo=True).all()
            locadores = Locador.query.filter_by(activo=True).all()
            
            print(f"   ✓ Empresas: {len(empresas)}")
            print(f"   ✓ Empleados activos: {len(empleados)}")
            print(f"   ✓ Locadores activos: {len(locadores)}")
            
            # Verificar columnas específicas
            print("\n📋 VERIFICANDO ESTRUCTURA...")
            empleado_ejemplo = Empleado.query.first()
            if empleado_ejemplo:
                print(f"   ✓ Empleado ejemplo: {empleado_ejemplo.nombres} {empleado_ejemplo.apellidos}")
                print(f"   ✓ Tipo de pago: {empleado_ejemplo.tipo_pago}")
                print(f"   ✓ Banco: {empleado_ejemplo.banco}")
                print(f"   ✓ Cuenta bancaria: {empleado_ejemplo.cuenta_bancaria}")
                print(f"   ✓ Descuento alimentos: S/. {empleado_ejemplo.descuento_alimentos}")
            
            print("\n" + "=" * 60)
            print("✅ SISTEMA FINAL INICIALIZADO EXITOSAMENTE")
            print("=" * 60)
            print("🎯 FUNCIONALIDADES COMPLETAS:")
            print("   ✓ Gestión de empresas (3 regímenes laborales)")
            print("   ✓ Gestión de empleados con todos los campos")
            print("   ✓ Gestión de locadores con todos los campos")
            print("   ✓ Tipos de pago (mensual/quincenal)")
            print("   ✓ Descuentos por alimentos (solo fin de mes)")
            print("   ✓ Información bancaria completa")
            print("   ✓ Cálculo de planillas por régimen")
            print("   ✓ Exportación a Excel")
            print("   ✓ Edición y eliminación de personal")
            print("   ✓ Carga masiva desde Excel")
            print("   ✓ Gestión de ausencias y deudas")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al inicializar sistema: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    if inicializar_sistema_final():
        print("\n🚀 Iniciando servidor Flask...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ No se pudo inicializar el sistema")
