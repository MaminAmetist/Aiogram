import sqlite3

connection_user = sqlite3.connect('users.db')
cursor_user = connection_user.cursor()


def initiate_db_users():
    cursor_user.execute("""
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    block BOOLEAN NOT NULL
    )
    """)
    connection_user.commit()


# Внесение админа в базу
def create_admin():
    cursor_user.execute("INSERT INTO Users ('username', 'user_id', 'block') VALUES (?, ?, ?)",
                        ('MaminAmetist', '130643448', 'False'))
    connection_user.commit()
    connection_user.close()


# Внесение пользователя в базу
def create_user(username, user_id, block=False):
    connection_user = sqlite3.connect('users.db')
    cursor_user = connection_user.cursor()
    cursor_user.execute("INSERT INTO Users ('username', 'user_id', 'block') VALUES (?, ?, ?)",
                        (f'{username}', f'{user_id}', f'{block}'))
    connection_user.commit()
    connection_user.close()


# Список ВСЕХ id пользователей
def get_users():
    connection_user = sqlite3.connect('users.db')
    cursor_user = connection_user.cursor()
    list_users = cursor_user.execute('SELECT user_id FROM Users').fetchall()
    connection_user.close()
    return list_users


# Поиск пользователя по user_id
def get_user_id(user_id):
    connection_user = sqlite3.connect('users.db')
    cursor_user = connection_user.cursor()
    user_list = cursor_user.execute('SELECT block FROM users WHERE user_id = ?',
                                    (f'{user_id}',)).fetchall()
    # connection_user.close()
    return user_list


# Список незаблокированных пользователей
def get_unban():
    connection_user = sqlite3.connect('users.db')
    cursor_user = connection_user.cursor()
    list_ban = cursor_user.execute('SELECT user_id FROM Users WHERE block = "False"').fetchall()
    connection_user.close()
    return list_ban


# Список заблокированных пользователей
def get_ban():
    connection_user = sqlite3.connect('users.db')
    cursor_user = connection_user.cursor()
    list_ban = cursor_user.execute('SELECT username FROM Users WHERE block = "True"').fetchall()
    connection_user.close()
    return list_ban


# Поиск заблокированных пользователей по user_id
def get_ban_id(user_id):
    connection_user = sqlite3.connect('users.db')
    cursor_user = connection_user.cursor()
    list_ban = cursor_user.execute(
        'SELECT username FROM Users WHERE block == "True" AND user_id == ?',
        (f'{user_id}',)).fetchall()
    connection_user.close()
    return list_ban


# Блокировка пользователя по user_id
def add_ban(user_id):
    connection_user = sqlite3.connect('users.db')
    cursor_user = connection_user.cursor()
    cursor_user.execute('UPDATE Users SET block = "True" WHERE user_id = ?', (f'{user_id}',))
    connection_user.commit()
    connection_user.close()


# РАЗБлокировка пользователя по user_id
def add_unban(user_id):
    connection_user = sqlite3.connect('users.db')
    cursor_user = connection_user.cursor()
    cursor_user.execute('UPDATE users SET block = "False" WHERE user_id = ?', (f'{user_id}',))
    connection_user.commit()
    connection_user.close()


# Вернуть имя
def get_username(user_id):
    connection_user = sqlite3.connect('users.db')
    cursor_user = connection_user.cursor()
    user = cursor_user.execute(
        'SELECT username FROM Users WHERE user_id == ?',
        (f'{user_id}',)).fetchall()
    connection_user.close()
    return user


initiate_db_users()
