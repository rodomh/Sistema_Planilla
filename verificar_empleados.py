import sqlite3

conn = sqlite3.connect('sispla.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(empleados)")
columns = cursor.fetchall()
print('Estructura de la tabla empleados:')
for col in columns:
    print(f'  {col[1]} - {col[2]}')
conn.close()
