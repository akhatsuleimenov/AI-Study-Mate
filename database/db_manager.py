import datetime
import sqlite3
from contextlib import contextmanager


class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.initialize_db()

    def initialize_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_thread (username TEXT PRIMARY KEY, thread_id TEXT)
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_requests (
                    username TEXT,
                    request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS authorized_users (
                    username TEXT PRIMARY KEY NOT NULL
                )
                """
            )
            conn.commit()

    @contextmanager
    def get_connection(self):
        """Provide a transactional scope around a series of operations."""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def is_user_authorized(self, username):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM authorized_users WHERE username = ?", (username.lower(),)
            )
            return cursor.fetchone() is not None

    def add_authorized_user(self, username):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM authorized_users WHERE username = ?", (username.lower(),)
            )
            if cursor.fetchone():
                return False  # User already exists
            cursor.execute(
                "INSERT INTO authorized_users (username) VALUES (?)",
                (username.lower(),),
            )
            conn.commit()
            return True

    def delete_authorized_user(self, username):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM authorized_users WHERE username = ?", (username.lower(),)
            )
            conn.commit()
            return True if cursor.rowcount > 0 else False

    def get_thread(self, username):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT thread_id FROM user_thread WHERE username = ?", (username,)
            )
            thread_id = cursor.fetchone()
            if thread_id:
                return thread_id[0]
            else:
                return None

    def save_thread(self, username, thread_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_thread (username, thread_id) VALUES (?, ?)",
                (username, thread_id),
            )
            conn.commit()

    def is_rate_limited(self, username, limit=100):
        current_time = datetime.datetime.now()
        hour_start = current_time.replace(minute=0, second=0, microsecond=0)
        hour_end = hour_start + datetime.timedelta(hours=1)

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT COUNT(*) FROM user_requests
                WHERE username = ? AND request_time >= ? AND request_time < ?
                """,
                (username, hour_start, hour_end),
            )
            count = cursor.fetchone()[0]
            return count >= limit

    def log_request(self, username):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_requests (username) VALUES (?)", (username,)
            )
            conn.commit()
