import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            print(f"Connection to {self.db_name} established.")
            return self.conn
        except sqlite3.Error as e:
            print(f"Error connecting to database {self.db_name}: {e}")
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            print(f"Connection to {self.db_name} closed.")
        # If an exception occurred, you might want to handle it here.
        # Returning True will suppress the exception.
        return False

# Using the DatabaseConnection context manager
db_file = 'users.db'
with DatabaseConnection(db_file) as conn:
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
            print("Users:")
            for row in results:
                print(row)
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
