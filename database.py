# database.py

import sqlite3
from utf_cleaner import UTFStringCleaner
cleaner = UTFStringCleaner()

class Database:
    def __init__(self, db_name='anon_bot.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                referral_code TEXT UNIQUE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER,
                recipient_id INTEGER,
                text TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_user(self, user_id, referral_code):
        try:
            cleaned_text = cleaner.clean(user_id)
        except:
            pass
        try:
            self.cursor.execute("INSERT INTO users (user_id, referral_code) VALUES (?, ?)", (user_id, referral_code))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass  # User already exists

    def get_user_by_referral_code(self, referral_code):
        self.cursor.execute("SELECT user_id FROM users WHERE referral_code = ?", (referral_code,))
        return self.cursor.fetchone()

    def save_message(self, sender_id, recipient_id, text):
        self.cursor.execute("INSERT INTO messages (sender_id, recipient_id, text) VALUES (?, ?, ?)", (sender_id, recipient_id, text))
        self.conn.commit()

    def get_messages_for_user(self, user_id):
        self.cursor.execute("SELECT text, sent_at FROM messages WHERE recipient_id = ?", (user_id,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()