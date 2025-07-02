
#!/usr/bin/python3
"""
Memory-efficient average age calculator using Python generators.
"""

import seed


def stream_user_ages():
    """
    Generator that yields ages of users one by one.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:
        yield row[0]

    cursor.close()
    connection.close()


def compute_average_age():
    """
    Computes the average age of users using generator, without loading all rows in memory.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        avg = total_age / count
        print(f"Average age of users: {avg:.2f}")
