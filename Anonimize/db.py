
import mysql.connector

def new_db_connection():
    connection = mysql.connector.connect(
        user='root',
        password='',
        host='127.0.0.1',
        database='restdb'
    )

    return connection