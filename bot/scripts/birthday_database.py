from datetime import datetime
import sqlite3
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "/app/bot/birthday-bot.db"

def connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_birthday_data():
    conn = connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS birthday_messages (
            id SERIAL PRIMARY KEY,
            name TEXT,
            date_sent TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()
        print("[DATABASE] Tabela 'birthday_messages' criada com sucesso.")
    except Exception as e:
        print(f"[DATABASE ERROR] Erro ao criar a tabela: {e}")
    finally:
        cursor.close()
        conn.close()


def has_sent_birthday_message(name):
    conn = connection()
    cursor = conn.cursor()

    today = datetime.now().strftime('%m-%d')

    cursor.execute('''
    SELECT 1 FROM birthday_messages WHERE name = ? AND date_sent = ?
    ''', (name, today))

    result = cursor.fetchone()
    conn.close()

    return result is not None

def mark_birthday_sent(name):
    conn = connection()
    cursor = conn.cursor()

    today = datetime.now().strftime('%m-%d')

    cursor.execute('''
    INSERT INTO birthday_messages (name, date_sent)
    VALUES (?, ?)
    ''', (name, today))

    conn.commit()
    conn.close()