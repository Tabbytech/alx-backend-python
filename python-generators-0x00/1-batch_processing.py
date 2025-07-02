#!/usr/bin/python3
"""
Batch processing users from SQL database using generators
"""

import mysql.connector


def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of users (list of dicts)
    """
    try:
        connection = mysql.connector.connect(
            user='root',
            password='$qlP@55w0rd!2o24#Db',  
            host='localhost',
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) FROM user_data")
        total_rows = cursor.fetchone()['COUNT(*)']
        
        for offset in range(0, total_rows, batch_size):
            cursor.execute(
                "SELECT * FROM user_data LIMIT %s OFFSET %s",
                (batch_size, offset)
            )
            batch = cursor.fetchall()
            if batch:
                yield batch

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return


def batch_processing(batch_size):
    """
    Processes each batch to print users with age > 25
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
