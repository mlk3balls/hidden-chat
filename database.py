# database.py

import sqlite3

def init_db():
    conn = sqlite3.connect("messages.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    username TEXT,
                    message TEXT
                )""")
    conn.commit()
    conn.close()

def save_message(user_id, username, message):
    conn = sqlite3.connect("messages.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages (user_id, username, message) VALUES (?, ?, ?)", (user_id, username, message))
    conn.commit()
    conn.close()

def get_all_messages():
    conn = sqlite3.connect("messages.db")
    c = conn.cursor()
    c.execute("SELECT id, message FROM messages")
    results = c.fetchall()
    conn.close()
    return results

def get_message_by_id(msg_id):
    conn = sqlite3.connect("messages.db")
    c = conn.cursor()
    c.execute("SELECT * FROM messages WHERE id = ?", (msg_id,))
    result = c.fetchone()
    conn.close()
    return result
