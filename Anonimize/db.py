
import mysql.connector

def new_db_connection():
    connection = mysql.connector.connect(
        user='jbroeren',
        password='Hello123!!*',
        host='localhost',
        port=3306,
        database='restdb'
    )

    return connection