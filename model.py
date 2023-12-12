import sqlite3
from sqlite3 import Error
import os

DB_FILE = "character_presets.db"

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        print(f"Connected to SQLite version {sqlite3.version}")
        return conn
    except Error as e:
        print(e)

    return conn


def create_presets_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS character_presets (
                user_id TEXT PRIMARY KEY,
                clothe INTEGER NOT NULL,
                hair INTEGER NOT NULL,
                expression INTEGER NOT NULL
            );
        ''')
        conn.commit()
    except Error as e:
        print(e)


def update_preset(conn, user_id, clothe, hair, expression):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO character_presets (user_id, clothe, hair, expression)
            VALUES (?, ?, ?, ?);
        ''', (user_id, clothe, hair, expression))
        conn.commit()
    except Error as e:
        print(e)


def retrieve_preset(conn, user_id):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT clothe, hair, expression
            FROM character_presets
            WHERE user_id = ?;
        ''', (user_id,))
        row = cursor.fetchone()
        if row:
            return {'clothe': row[0], 'hair': row[1], 'expression': row[2]}
    except Error as e:
        print(e)


def initialize_database():
    conn = create_connection()
    if conn:
        create_presets_table(conn)
        conn.close()


initialize_database()
