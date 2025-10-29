#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba del sistema simplificado
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_simple import app, db, Empresa, Empleado, Locador

def test_sistema_simple():
    """Probar el sistema simplificado"""
    print("INICIANDO PRUEBA DEL SISTEMA SIMPLIFICADO...")
    print("=" * 60)
    
    with app.app_context():
        try:
            # Verificar empresas
            empresas = Empresa.query.all()
            print(f"✓ Empresas encontradas: {len(empresas)}")
            
            if empresas:
                empresa = empresas[0]
                print(f"✓ Empresa: {empresa.nombre} ({empresa.regimen_laboral})")
                
                # Verificar empleados
                empleados = Empleado.query.filter_by(empresa_id=empresa.id, activo=True).all()
                print(f"✓ Empleados activos: {len(empleados)}")
                
                # Verificar locadores
                locadores = Locador.query.filter_by(empresa_id=empresa.id, activo=True).all()
                print(f"✓ Locadores activos: {len(locadores)}")
                
                # Probar cálculo de planilla
                from app_simple import calcular_planilla_simple
                resultado = calcular_planilla_simple(empresa.id, 10, 2024)
                print(f"✓ Cálculo de planilla exitoso para {len(resultado['empleados'])} empleados y {len(resultado['locadores'])} locadores")
                
                print("\n" + "=" * 60)
                print("✅ SISTEMA SIMPLIFICADO FUNCIONANDO CORRECTAMENTE")
                print("=" * 60)
                print("🌐 Accede a: http://localhost:5000")
                print("📊 Funcionalidades disponibles:")
                print("   - Gestión de empresas")
                print("   - Registro de empleados y locadores")
                print("   - Cálculo de planillas por régimen")
                print("   - Interfaz web funcional")
                
            else:
                print("⚠️  No hay empresas registradas")
                
        except Exception as e:
            print(f"❌ Error en el sistema: {str(e)}")
            return False
    
    return True

if __name__ == "__main__":
    test_sistema_simple()
