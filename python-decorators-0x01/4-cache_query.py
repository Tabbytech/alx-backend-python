import time
import sqlite3
import functools


query_cache = {}

"""your code goes here"""
def cache_query(func):
    """Caches query results based on the SQL query string."""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print(f"Cache hit for query: {query}")
            return query_cache[query]
        else:
            print(f"Cache miss for query: {query}")
            result = func(conn, query, *args, **kwargs)
            query_cache[query] = result
            return result
    return wrapper

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

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print("First call results:", users)

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print("Second call results:", users_again)

#### Third call with a different query
users_different = fetch_users_with_cache(query="SELECT COUNT(*) FROM users")
print("Third call results (different query):", users_different)
