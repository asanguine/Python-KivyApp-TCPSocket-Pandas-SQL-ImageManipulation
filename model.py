import sqlite3
from sqlite3 import Error
import os
import uuid
from datetime import datetime

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

def generate_user_id():
    return str(uuid.uuid4())


def retrieve_user_id(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM character_presets LIMIT 1;')
        row = cursor.fetchone()
        if row:
            return row[0]
    except Error as e:
        print(e)


def add_user(conn, user_id, clothe, hair, expression):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO connected_users (user_id, clothe, hair, expression)
            VALUES (?, ?, ?, ?);
        ''', (user_id, clothe, hair, expression))
        conn.commit()
    except Error as e:
        print(e)


def remove_user(conn, user_id):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM connected_users WHERE user_id = ?;
        ''', (user_id,))
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


####  STUDY SESSION STATS ()()()()()()()

def create_study_sessions_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS study_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                date TEXT,
                duration INTEGER,
                FOREIGN KEY (user_id) REFERENCES character_presets (user_id)
            );
        ''')
        conn.commit()
    except Error as e:
        print(e)


def get_study_data(conn, user_id):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT date, duration
            FROM study_sessions
            WHERE user_id = ?;
        ''', (user_id,))
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(e)


def get_aggregated_study_data(conn, user_id):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT date, SUM(duration) as total_duration
            FROM study_sessions
            WHERE user_id = ?
            GROUP BY date;
        ''', (user_id,))
        rows = cursor.fetchall()
        return {(row[0], row[1]) for row in rows}
    except Error as e:
        print(e)


def add_study_session(conn, user_id, duration):
    try:
        cursor = conn.cursor()
        date_today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute('''
            INSERT INTO study_sessions (user_id, date, duration)
            VALUES (?, ?, ?);
        ''', (user_id, date_today, duration))
        conn.commit()
    except Error as e:
        print(e)

############

def initialize_database():
    conn = create_connection()
    if conn:
        create_presets_table(conn)
        create_study_sessions_table(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM character_presets")
        count = cursor.fetchone()[0]
        if count == 0:
            user_id = generate_user_id()
            cursor.execute('''
                INSERT INTO character_presets (user_id, clothe, hair, expression)
                VALUES (?, 1, 1, 1);
            ''', (user_id,))
            conn.commit()
        conn.close()


initialize_database()
