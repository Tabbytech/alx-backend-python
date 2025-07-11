import time
import sqlite3
import functools

#### paste your with_db_decorator here
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

""" your code goes here"""
def retry_on_failure(retries=3, delay=2):
    """Retries the decorated function if it raises an exception."""
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except sqlite3.Error as e:
                    attempts += 1
                    print(f"Attempt {attempts} failed with error: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
            print(f"All {retries} retry attempts failed.")
            raise  # Re-raise the last exception
        return wrapper
    return decorator_retry

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)
