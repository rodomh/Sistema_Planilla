#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar contenido de la base de datos
"""

import sqlite3

def verificar_bd():
    """Verificar contenido de la base de datos"""
    print("VERIFICANDO BASE DE DATOS...")
    print("=" * 40)
    
    try:
        conn = sqlite3.connect('planillas_peru.db')
        cursor = conn.cursor()
        
        # Listar tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tablas encontradas: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Verificar contenido de cada tabla
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"\n{table_name}: {count} registros")
            
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                rows = cursor.fetchall()
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in cursor.fetchall()]
                print(f"  Columnas: {', '.join(columns)}")
                print(f"  Primeros registros:")
                for row in rows:
                    print(f"    {row}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    verificar_bd()
