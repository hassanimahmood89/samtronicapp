import sqlite3


def init_db():
    conn = sqlite3.connect("samtronic.db")
    c = conn.cursor()

    c.execute(
        """CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT
    )"""
    )

    c.execute(
        """CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        quantity INTEGER,
        buy_price TEXT,
        sell_price TEXT
    )"""
    )

    c.execute(
        """CREATE TABLE IF NOT EXISTS repairs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        device TEXT,
        problem TEXT,
        status TEXT,
        cost TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )"""
    )

    c.execute(
        """CREATE TABLE IF NOT EXISTS repair_parts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        repair_id INTEGER,
        part_id INTEGER,
        quantity_used INTEGER,
        FOREIGN KEY (repair_id) REFERENCES repairs(id),
        FOREIGN KEY (part_id) REFERENCES inventory(id)
    )"""
    )

    conn.commit()
    conn.close()
