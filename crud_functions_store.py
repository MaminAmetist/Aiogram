import sqlite3


def initiate_db_store():
    connection_store = sqlite3.connect('stores.db')
    cursor_store = connection_store.cursor()
    cursor_store.execute("""
    CREATE TABLE IF NOT EXISTS Stores(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    address TEXT
    )
    """)
    connection_store.commit()


# Внесение данных в базу
def create_new_store(title, address):
    connection_store = sqlite3.connect('stores.db')
    cursor_store = connection_store.cursor()
    cursor_store.execute("INSERT INTO Stores ('title', 'address') VALUES (?, ?)",
                         (f'{title}', f'{address}'))
    connection_store.commit()
    connection_store.close()


# Показываем списковое
def get_stores():
    connection_store = sqlite3.connect('stores.db')
    cursor_store = connection_store.cursor()
    list_stores = cursor_store.execute('SELECT title, address FROM Stores').fetchall()
    connection_store.close()
    return list_stores


# Удалить запись из списка
def del_store(title):
    connection_store = sqlite3.connect('stores.db')
    cursor_store = connection_store.cursor()
    cursor_store.execute('DELETE FROM Stores WHERE title = ?', (f'{title}',))
    connection_store.commit()
    connection_store.close()


initiate_db_store()
