# db.py
import sqlite3

def init_db():
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            personal_phone TEXT,
            score INTEGER,
            moves INTEGER,
            time INTEGER
        )
    """)
    conn.commit()
    conn.close()

def save_lead(name, email, phone, score, moves, time):
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO leads (name, email, personal_phone, score, moves, time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, email, phone, score, moves, time))
    conn.commit()
    conn.close()
