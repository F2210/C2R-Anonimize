import mysql.connector
from mysql.connector import Error

def new_db_connection():

    try:

        connection = mysql.connector.connect(
            user='jbroeren',
            password='Hello123!!*',
            host='192.168.1.175',
            database='restdb'
        )

    except Error as e:
        print("connection failed")
        print(e)

    if connection is not None and connection.is_connected():
        return connection

    else:
        print("no connection")