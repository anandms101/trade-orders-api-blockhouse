import sqlite3

"""
Establishes a connection to the SQLite database.

Returns:
    sqlite3.Connection: A connection object to the SQLite database.
"""
def get_connection():
    return sqlite3.connect("orders.db")

"""
Initializes the database by creating the 'orders' table if it does not exist.
The 'orders' table contains the following columns:
    - id: An integer primary key that autoincrements.
    - symbol: A text field for the order symbol.
    - price: A real number for the order price.
    - quantity: An integer for the order quantity.
    - order_type: A text field for the type of order.
"""
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            order_type TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

"""
Initializes the database when this module is imported.
"""
init_db()
