import sqlite3
from typing import Optional, Tuple, Any


class Database:
    def __init__(self, url: str):
        self.url = url

    def create_database(self) -> None:
        """
        Create the SQLite database and users table if it doesn't exist.
        Opens and closes its own connection to avoid cross-thread SQLite errors.
        """
        try:
            with sqlite3.connect(self.url, check_same_thread=False) as conn:
                cursor = conn.cursor()
                # create the table if it doesn't exist (atomic and safe across threads)
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, lang INTEGER NOT NULL CHECK (lang IN (0, 1)) )"
                )
                conn.commit()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def create_user(self, username: str, lang: int) -> str:
        """
        Create a new user if not exists. Uses its own connection per call.
        """
        try:
            with sqlite3.connect(self.url, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
                if cursor.fetchone():
                    return "User already exists"
                cursor.execute("INSERT INTO users (username, lang) VALUES (?, ?)", (username, int(lang)))
                conn.commit()
                return "User created"
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return "Error"

    def get_user_by_username(self, username: str) -> Optional[Tuple[Any, ...]]:
        """
        Returns the user row as a tuple or None.
        """
        try:
            with sqlite3.connect(self.url, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
                return cursor.fetchone()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def get_user_lang(self, username: str) -> Optional[int]:
        """
        Returns the `lang` value for the given username or None if not found.
        """
        try:
            with sqlite3.connect(self.url, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT lang FROM users WHERE username = ?", (username,))
                row = cursor.fetchone()
                return row[0] if row else None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def change_user_lang(self, username: str) -> int:
        """
        Toggles the user's lang between 0 and 1. Returns True on success, False otherwise.
        """
        try:
            with sqlite3.connect(self.url, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT lang FROM users WHERE username = ?", (username,))
                row = cursor.fetchone()
                if not row:
                    return False
                oldLang = row[0]
                newLang = 1 if oldLang == 0 else 0
                cursor.execute("UPDATE users SET lang = ? WHERE username = ?", (int(newLang), username))
                conn.commit()
                return newLang
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

