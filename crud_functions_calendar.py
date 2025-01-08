import sqlite3

connection_calendar = sqlite3.connect('calendars.db')
cursor_calendar = connection_calendar.cursor()


def initiate_db_calendars():
    cursor_calendar.execute("""
    CREATE TABLE IF NOT EXISTS Calendars(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    date TEXT NOT NULL, 
    repeat TEXT NOT NULL, 
    date_create TIMESTAMP DEFAULT (datetime('now','localtime'))
    )
    """)
    connection_calendar.commit()


# Внесение мероприятия в базу
def create_event(user_id, title, date, repeat):
    connection_calendar = sqlite3.connect('calendars.db')
    cursor_calendar = connection_calendar.cursor()
    cursor_calendar.execute("INSERT INTO Calendars ('user_id', 'title', 'date', 'repeat') VALUES (?, ?, ?, ?)",
                            (f'{user_id}', f'{title}', f'{date}', f'{repeat}'))
    connection_calendar.commit()
    connection_calendar.close()


# Показываем мероприятия на день
def get_event_today(user_id, date):
    connection_calendar = sqlite3.connect('calendars.db')
    cursor_calendar = connection_calendar.cursor()
    list_event = cursor_calendar.execute(
        'SELECT title FROM Calendars WHERE user_id = ? AND date = ?',
        (f'{user_id}', f'{date}')).fetchall()
    connection_calendar.close()
    return list_event


# Показываем все мероприятия
def get_event():
    connection_calendar = sqlite3.connect('calendars.db')
    cursor_calendar = connection_calendar.cursor()
    list_event = cursor_calendar.execute(
        'SELECT title, date FROM Calendars').fetchall()
    connection_calendar.close()
    return list_event


# Удалить запись из календаря
def del_event(title, date):
    connection_calendar = sqlite3.connect('calendars.db')
    cursor_calendar = connection_calendar.cursor()
    cursor_calendar.execute('DELETE FROM Calendars WHERE title = ? and date = ?',
                            (f'{title}', f'{date}'))
    connection_calendar.commit()
    connection_calendar.close()


# Вернуть репит по титлу и дате
def get_repeat(title, date):
    connection_calendar = sqlite3.connect('calendars.db')
    cursor_calendar = connection_calendar.cursor()

    list_repeat = cursor_calendar.execute(
        'SELECT repeat FROM Calendars WHERE title = ? AND date = ?',
        (f'{title}', f'{date}')
    ).fetchall()
    connection_calendar.close()
    return list_repeat


# Изменить запись
def change_event(date, title):
    connection_calendar = sqlite3.connect('calendars.db')
    cursor_calendar = connection_calendar.cursor()
    cursor_calendar.execute('UPDATE Calendars SET date = ? WHERE title = ?', (f'{date}', f'{title}'))
    connection_calendar.commit()
    connection_calendar.close()


initiate_db_calendars()
