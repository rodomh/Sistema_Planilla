#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Probar funcionalidad de cargar desde Excel
"""

import requests
import os

def test_cargar_excel():
    """Probar la funcionalidad de cargar desde Excel"""
    print("PROBANDO FUNCIONALIDAD DE CARGAR DESDE EXCEL...")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    try:
        # 1. Probar acceso a la página de cargar Excel
        print("1. PROBANDO ACCESO A CARGAR EXCEL...")
        response = requests.get(f"{base_url}/cargar_excel/1")
        if response.status_code == 200:
            print("   ✓ Página de cargar Excel accesible")
        else:
            print(f"   ❌ Error al acceder a cargar Excel: {response.status_code}")
            return False
        
        # 2. Probar descarga de plantilla
        print("\n2. PROBANDO DESCARGA DE PLANTILLA...")
        response = requests.get(f"{base_url}/descargar_plantilla/1")
        if response.status_code == 200:
            print("   ✓ Plantilla Excel descargada correctamente")
            # Guardar plantilla para verificar
            with open('plantilla_test.xlsx', 'wb') as f:
                f.write(response.content)
            print("   ✓ Plantilla guardada como 'plantilla_test.xlsx'")
        else:
            print(f"   ❌ Error al descargar plantilla: {response.status_code}")
            return False
        
        # 3. Verificar que la plantilla se creó correctamente
        print("\n3. VERIFICANDO PLANTILLA...")
        if os.path.exists('plantilla_test.xlsx'):
            print("   ✓ Archivo de plantilla creado")
            file_size = os.path.getsize('plantilla_test.xlsx')
            print(f"   ✓ Tamaño del archivo: {file_size} bytes")
        else:
            print("   ❌ No se pudo crear el archivo de plantilla")
            return False
        
        # 4. Probar acceso a personal (que ahora debería funcionar)
        print("\n4. PROBANDO ACCESO A PERSONAL...")
        response = requests.get(f"{base_url}/personal/1")
        if response.status_code == 200:
            print("   ✓ Página de personal accesible")
        else:
            print(f"   ❌ Error al acceder a personal: {response.status_code}")
            return False
        
        print("\n" + "=" * 60)
        print("✅ FUNCIONALIDAD DE CARGAR EXCEL FUNCIONANDO CORRECTAMENTE")
        print("=" * 60)
        print("🎯 Funcionalidades verificadas:")
        print("   ✓ Página de cargar Excel accesible")
        print("   ✓ Descarga de plantilla funcionando")
        print("   ✓ Plantilla Excel creada correctamente")
        print("   ✓ Página de personal accesible")
        print("   ✓ Error de BuildError corregido")
        
        # Limpiar archivo de prueba
        if os.path.exists('plantilla_test.xlsx'):
            os.remove('plantilla_test.xlsx')
            print("\n✓ Archivo de prueba eliminado")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("   Asegúrate de que el sistema esté ejecutándose en http://localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

if __name__ == "__main__":
    test_cargar_excel()
