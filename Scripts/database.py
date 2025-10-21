import sqlite3

# Connect to a file-based database (creates if it doesn't exist)
# conn = sqlite3.connect("Database/users.db")

# # Connect to an in-memory database
# # conn = sqlite3.connect(':memory:')
# cursor = conn.cursor()
# cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, lang INTEGER NOT NULL CHECK (lang IN (0, 1)) )")
# cursor.execute("INSERT INTO users (name, lang) VALUES ('Alice', True)")
# conn.commit()

# cursor.execute("SELECT * FROM users")
# rows = cursor.fetchall()
# for row in rows:
#     print(row)


class Database:
    def __init__(self, url):
        self.url = url
        self.conn = None
        self.cursor = None

    def create_database(self):
        self.conn = sqlite3.connect(self.url)
        self.cursor = self.conn.cursor()
        # Check whether the 'users' table exists
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if self.cursor.fetchone():
            print("table exists")
            return
        else:
            # create the table if it doesn't exist
            print("creating users table")
            self.cursor.execute(
                "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, lang INTEGER NOT NULL CHECK (lang IN (0, 1)) )"
            )
            self.conn.commit()

    def create_user(self, username, lang):
        # Use parameterized queries to avoid SQL injection and check existence properly
        self.cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,)) # pyright: ignore[reportOptionalMemberAccess]
        if self.cursor.fetchone(): # type: ignore
            return "User already exists"
        self.cursor.execute("INSERT INTO users (username, lang) VALUES (?, ?)", (username, int(lang))) # type: ignore
        self.conn.commit() # type: ignore
        return "User created"

    def get_user_by_username(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,)) # type: ignore
        return self.cursor.fetchone()# type: ignore
    
    def get_user_lang(self,username):
        self.cursor.execute("SELECT lang FROM users WHERE username = ?",(username,))# type: ignore
        return self.cursor.fetchone()# type: ignore 
    
    def update_user_lang(self,username,lang):
        self.cursor.execute("UPDATE users SET lang = ? WHERE username = ?",(int(lang),username,))# type: ignore
        self.conn.commit()# type: ignore 
        return
    
db = Database("Database/users.db")

db.create_database()
# print(db.create_user("mehdi",0))  
print(db.get_user_by_username("mehdi"))
print(db.get_user_lang("mehdi"))
print(db.update_user_lang("mehdi",0))
print(db.get_user_by_username("mehdi"))