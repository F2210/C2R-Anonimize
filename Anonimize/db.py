
import mysql.connector

def new_db_connection():
    connection = mysql.connector.connect(
        user='root',
        password='',
        host='localhost',
        database='restdb'
    )

    return connection