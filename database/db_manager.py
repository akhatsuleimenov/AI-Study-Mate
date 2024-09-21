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
                CREATE TABLE IF NOT EXISTS user_thread (user_id INTEGER PRIMARY KEY, thread_id TEXT)
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_requests (
                    user_id INTEGER,
                    request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS authorized_users (
                    user_id INTEGER PRIMARY KEY
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

    def is_user_authorized(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM authorized_users WHERE user_id = ?", (user_id,)
            )
            return cursor.fetchone() is not None

    def add_authorized_user(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM authorized_users WHERE user_id = ?", (user_id,)
            )
            if cursor.fetchone():
                return False  # User already exists
            cursor.execute(
                "INSERT INTO authorized_users (user_id) VALUES (?)", (user_id,)
            )
            conn.commit()
            return True

    def get_thread(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT thread_id FROM user_thread WHERE user_id = ?", (user_id,)
            )
            thread_id = cursor.fetchone()
            if thread_id:
                return thread_id[0]
            else:
                return None

    def save_thread(self, user_id, thread_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_thread (user_id, thread_id) VALUES (?, ?)",
                (user_id, thread_id),
            )
            conn.commit()

    def is_rate_limited(self, user_id, limit=100):
        current_time = datetime.datetime.now()
        hour_start = current_time.replace(minute=0, second=0, microsecond=0)
        hour_end = hour_start + datetime.timedelta(hours=1)

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT COUNT(*) FROM user_requests
                WHERE user_id = ? AND request_time >= ? AND request_time < ?
                """,
                (user_id, hour_start, hour_end),
            )
            count = cursor.fetchone()[0]
            return count >= limit

    def log_request(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user_requests (user_id) VALUES (?)", (user_id,))
            conn.commit()
