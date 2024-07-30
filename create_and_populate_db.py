import sqlite3

def create_and_populate_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS equipment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        availability TEXT NOT NULL,
        price REAL NOT NULL
    )
    ''')

    equipment_data = [
        ('Camera', 'Video', 'Available', 1200.00),
        ('Microphone', 'Audio', 'Unavailable', 150.00),
        ('Tripod', 'Accessory', 'Available', 300.00),
        ('Lighting Kit', 'Lighting', 'Available', 500.00)
    ]

    cursor.executemany('''
    INSERT INTO equipment (name, type, availability, price)
    VALUES (?, ?, ?, ?)
    ''', equipment_data)

    conn.commit()
    conn.close()

create_and_populate_db('equipment_rental.db')
