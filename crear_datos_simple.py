#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crear datos de ejemplo para el sistema simplificado
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_simple import app, db, Empresa, Empleado, Locador
from datetime import date, datetime

def crear_datos_ejemplo():
    """Crear datos de ejemplo"""
    print("CREANDO DATOS DE EJEMPLO...")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Crear empresa
            empresa = Empresa(
                nombre="Inversiones IH SRL",
                ruc="20123456789",
                regimen_laboral="microempresa",
                direccion="Av. Principal 123, Lima",
                telefono="987654321",
                email="info@inversionesih.com"
            )
            db.session.add(empresa)
            db.session.commit()
            print("✓ Empresa creada: Inversiones IH SRL")
            
            # Crear empleados
            empleados_data = [
                {
                    'nombres': 'Juan Carlos',
                    'apellidos': 'Pérez García',
                    'dni': '12345678',
                    'sueldo_base': 1500.0,
                    'fecha_ingreso': date(2024, 1, 15),
                    'tipo_pension': 'ONP'
                },
                {
                    'nombres': 'María Elena',
                    'apellidos': 'López Silva',
                    'dni': '87654321',
                    'sueldo_base': 2000.0,
                    'fecha_ingreso': date(2024, 2, 1),
                    'tipo_pension': 'AFP',
                    'afp_codigo': 'PRIMA'
                }
            ]
            
            for emp_data in empleados_data:
                empleado = Empleado(
                    empresa_id=empresa.id,
                    **emp_data
                )
                db.session.add(empleado)
            
            print("✓ Empleados creados: 2")
            
            # Crear locadores
            locadores_data = [
                {
                    'nombres': 'Ana María',
                    'apellidos': 'Rodríguez Castro',
                    'dni': '55667788',
                    'monto_mensual': 2500.0,
                    'fecha_inicio': date(2024, 1, 20),
                    'suspendido': False
                },
                {
                    'nombres': 'Luis',
                    'apellidos': 'Herrera Morales',
                    'dni': '99887766',
                    'monto_mensual': 3000.0,
                    'fecha_inicio': date(2024, 2, 15),
                    'suspendido': False
                }
            ]
            
            for loc_data in locadores_data:
                locador = Locador(
                    empresa_id=empresa.id,
                    **loc_data
                )
                db.session.add(locador)
            
            print("✓ Locadores creados: 2")
            
            db.session.commit()
            
            print("\n" + "=" * 50)
            print("✅ DATOS DE EJEMPLO CREADOS EXITOSAMENTE")
            print("=" * 50)
            print("🌐 Accede a: http://localhost:5000")
            print("📊 Datos disponibles:")
            print("   - 1 empresa (Microempresa)")
            print("   - 2 empleados")
            print("   - 2 locadores")
            print("   - Sistema listo para usar")
            
        except Exception as e:
            print(f"❌ Error al crear datos: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    crear_datos_ejemplo()
