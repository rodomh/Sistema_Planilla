#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Probar que las rutas de Excel estén definidas correctamente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_completo import app

def test_rutas_excel():
    """Probar que las rutas de Excel estén definidas"""
    print("PROBANDO RUTAS DE EXCEL...")
    print("=" * 40)
    
    with app.app_context():
        try:
            # Obtener todas las rutas registradas
            rules = []
            for rule in app.url_map.iter_rules():
                rules.append(rule.rule)
            
            print("Rutas registradas en la aplicación:")
            for rule in sorted(rules):
                print(f"  - {rule}")
            
            # Verificar rutas específicas de Excel
            rutas_excel = [
                '/cargar_excel/<int:empresa_id>',
                '/descargar_plantilla/<int:empresa_id>',
                '/exportar_excel/<int:empresa_id>'
            ]
            
            print(f"\nVerificando rutas de Excel:")
            for ruta in rutas_excel:
                if ruta in rules:
                    print(f"  ✓ {ruta} - Definida")
                else:
                    print(f"  ❌ {ruta} - No encontrada")
            
            # Verificar que no hay errores de sintaxis
            print(f"\n✓ Aplicación Flask cargada correctamente")
            print(f"✓ Total de rutas registradas: {len(rules)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al cargar la aplicación: {str(e)}")
            return False

if __name__ == "__main__":
    test_rutas_excel()
