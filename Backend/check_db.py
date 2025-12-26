import sqlite3

try:
    conn = sqlite3.connect('hindi_books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = cursor.fetchall()
    print('Database tables:', tables)
    conn.close()
    print('Database is accessible')
except Exception as e:
    print('Error:', e)