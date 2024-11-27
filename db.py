import os
import sqlite3


if not os.path.exists('instance'):
    os.makedirs('instance')


connection = sqlite3.connect('instance/menu.db')
cursor = connection.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        price REAL NOT NULL
    )
''')


menu_items = [
    ('Зоряний дракон', 'Грета мандарин та синій буряк', 538.22),
    ('Супер-сирна фантазія', 'Кубики апельсина з кремом пшениці', 455.36),
    ('Рай для очей', 'Кисломолочний нектар з шафраном', 621.09),
    ('Лісовий елемент', 'Розмаринова риба з персиковим соусом', 473.50),
    ('Плодовий вибух', 'Жовті малини з інжиром на майонезі', 296.72),
    ('Червона зірка', 'Долина перцю з рисовими пластівцями', 698.13),
    ('Гармонія снігу', 'Лимон та біле кефірове масло', 347.88),
    ('Тропічний острів', 'Маракуйя та квасоля з часником', 629.46),
    ('Темна хмара', 'Тортельїні з бананом та морквою', 510.90)
]


cursor.executemany('''
    INSERT INTO menu_items (name, description, price) 
    VALUES (?, ?, ?)
''', menu_items)


connection.commit()
connection.close()

print("База даних 'menu.db' створена, і дані успішно додані до таблиці 'menu_items'!")
