
import mysql.connector

def new_db_connection():
    connection = mysql.connector.connect(
        user='root',
        password='',
        host='localhost',
        port=3306,
        database='restdb'
    )

    return connection

new_db_connection()