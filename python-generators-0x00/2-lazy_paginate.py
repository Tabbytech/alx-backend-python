#!/usr/bin/python3
"""
Lazy pagination: Generator loads one page of users at a time using SQL LIMIT and OFFSET.
"""

import seed


def paginate_users(page_size, offset):
    """
    Fetches a page of users from the user_data table.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator function that yields one page at a time lazily.
    Only loads the next page when needed.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
