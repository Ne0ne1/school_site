import sqlite3

# Подключение к базе данных (файл создастся автоматически)
conn = sqlite3.connect('database.db')  
cursor = conn.cursor()

# Создание таблицы "модератор"
cursor.execute('''
CREATE TABLE IF NOT EXISTS модератор (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    класс TEXT NOT NULL,
    предмет TEXT NOT NULL
);
''')

# Создание индекса (для ускорения поиска)
cursor.execute('CREATE INDEX IF NOT EXISTS idx_класс ON модератор (класс);')

# Пример добавления данных
cursor.execute("INSERT INTO модератор (класс, предмет) VALUES (?, ?)", ('10А', 'Математика'))
cursor.execute("INSERT INTO модератор (класс, предмет) VALUES (?, ?)", ('8Б', 'Физика'))

# Сохраняем изменения
conn.commit()

# Закрываем соединение
conn.close()

import sqlite3

# Подключаемся к базе данных (файл 'subjects.db' создастся автоматически)
conn = sqlite3.connect('subjects.db')
cursor = conn.cursor()

# Создаём таблицу 'предметы'
cursor.execute('''
CREATE TABLE IF NOT EXISTS предметы (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    classes TEXT NOT NULL
);
''')

# Пример добавления данных
cursor.execute("INSERT INTO предметы (title, classes) VALUES (?, ?)", ('Математика', '9А, 10Б, 11В'))
cursor.execute("INSERT INTO предметы (title, classes) VALUES (?, ?)", ('Физика', '8А, 9Б, 10В'))
cursor.execute("INSERT INTO предметы (title, classes) VALUES (?, ?)", ('Информатика', '7А, 8Б, 9В'))

# Сохраняем изменения
conn.commit()

# Проверяем содержимое таблицы
print("Содержимое таблицы 'предметы':")
cursor.execute("SELECT * FROM предметы")
for row in cursor.fetchall():
    print(row)

# Закрываем соединение
conn.close()


import sqlite3

# Подключаемся к базе данных (файл 'school.db' создастся автоматически)
conn = sqlite3.connect('school.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS класс (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE  # Название класса (например, "10А")
);
''')

# Пример добавления данных
classes = ['5А', '6Б', '7В', '8Г', '9Д', '10А']
for class_title in classes:
    cursor.execute("INSERT OR IGNORE INTO класс (title) VALUES (?)", (class_title,))

# Сохраняем изменения
conn.commit()

# Проверяем содержимое таблицы
print("Содержимое таблицы 'класс':")
cursor.execute("SELECT * FROM класс")
for row in cursor.fetchall():
    print(row)

# Закрываем соединение
conn.close()


import sqlite3
import hashlib

# Создаем базу данных и подключаемся
conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# Создаем таблицу классов (если её нет)
cursor.execute('''
CREATE TABLE IF NOT EXISTS класс (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE
)''')

# Создаем таблицу учеников
cursor.execute('''
CREATE TABLE IF NOT EXISTS ученик (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER NOT NULL,
    fio TEXT NOT NULL,
    login TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    FOREIGN KEY (class_id) REFERENCES класс(id)
)''')

# Добавляем тестовые классы (если их нет)
cursor.executemany(
    "INSERT OR IGNORE INTO класс (title) VALUES (?)",
    [('5А',), ('6Б',), ('7В',)]
)

# Функция для хеширования паролей
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Добавляем тестовых учеников
students = [
    (1, 'Иванов Иван Иванович', 'ivanov', hash_password('12345')),
    (1, 'Петрова Анна Сергеевна', 'petrova', hash_password('qwerty')),
    (2, 'Сидоров Алексей Петрович', 'sidorov', hash_password('password'))
]

cursor.executemany(
    "INSERT OR IGNORE INTO ученик (class_id, fio, login, password) VALUES (?, ?, ?, ?)",
    students
)

# Сохраняем изменения
conn.commit()

# Проверяем содержимое
print("Классы:")
cursor.execute("SELECT * FROM класс")
for row in cursor.fetchall():
    print(row)

print("\nУченики:")
cursor.execute("SELECT ученик.id, класс.title, ученик.fio, ученик.login FROM ученик JOIN класс ON ученик.class_id = класс.id")
for row in cursor.fetchall():
    print(row)

# Закрываем соединение
conn.close()