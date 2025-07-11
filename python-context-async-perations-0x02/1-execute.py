import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self.cursor.execute(self.query, self.params)
            self.results = self.cursor.fetchall()
            print(f"Executed query: '{self.query}' with parameters: {self.params}")
            return self.results
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            if self.conn:
                self.conn.rollback()
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
            print("Cursor closed.")
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
        # Allow exceptions to propagate
        return False

# Using the ExecuteQuery context manager
db_file = 'users.db'
query_string = "SELECT * FROM users WHERE age > ?"
query_parameters = (25,)

with ExecuteQuery(db_file, query_string, query_parameters) as users_over_25:
    if users_over_25:
        print("Users over 25:")
        for user in users_over_25:
            print(user)
