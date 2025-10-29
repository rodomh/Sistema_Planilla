import sqlite3

conn = sqlite3.connect('sispla.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tablas en la base de datos:')
for table in tables:
    print(f'  {table[0]}')
conn.close()
