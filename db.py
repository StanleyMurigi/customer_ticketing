import sqlite3
from config import DB

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tickets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  prefix TEXT,
                  number INTEGER,
                  counter INTEGER,
                  status TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  served_at TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS counters
                 (id INTEGER PRIMARY KEY, name TEXT)''')
    conn.commit()
    conn.close()

def add_ticket_to_db(prefix, number, counter):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO tickets (prefix, number, counter, status) VALUES (?, ?, ?, ?)",
              (prefix, number, counter, 'waiting'))
    conn.commit()
    conn.close()

def mark_served_in_db(prefix, number):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("UPDATE tickets SET status='served', served_at=CURRENT_TIMESTAMP WHERE prefix=? AND number=?",
              (prefix, number))
    conn.commit()
    conn.close()

def get_unserved_tickets_for_counter(counter):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        "SELECT prefix, number, created_at FROM tickets WHERE counter=? AND status='waiting' ORDER BY created_at ASC",
        (counter,)
    )
    rows = c.fetchall()
    conn.close()
    return rows  # List of (prefix, number, created_at)

def get_next_ticket_for_counter(counter):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        "SELECT prefix, number FROM tickets WHERE counter=? AND status='waiting' ORDER BY created_at ASC LIMIT 1",
        (counter,)
    )
    row = c.fetchone()
    conn.close()
    return row  # (prefix, number) or None
