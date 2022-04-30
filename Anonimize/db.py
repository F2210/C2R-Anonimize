
import mysql.connector

def new_db_connection():
    connection = mysql.connector.connect(
        user='root',
        host='localhost',
        port=3306,
        database='restdb'
    )

    return connection