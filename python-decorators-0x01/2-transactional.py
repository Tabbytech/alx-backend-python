import sqlite3
import functools

def with_db_connection(func):
    """Opens a database connection, passes it to the function and closes it afterward."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect('users.db')
            # Pass the connection object as the first argument
            result = func(conn, *args, **kwargs)
            return result
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn:
                conn.close()
                print("Database connection closed.")
    return wrapper

def transactional(func):
    """Ensures a function running a database operation is wrapped inside a transaction."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            conn.execute("BEGIN TRANSACTION")
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("Transaction committed.")
            return result
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Transaction rolled back due to error: {e}")
            return None
        except Exception as e:
            conn.rollback()
            print(f"Transaction rolled back due to unexpected error: {e}")
            raise  # Re-raise the unexpected exception
        finally:
            pass # Connection closing is handled by with_db_connection
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

#### Update user's email with automatic transaction handling
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
