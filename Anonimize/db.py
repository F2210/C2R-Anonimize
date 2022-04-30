import mysql.connector
from mysql.connector import Error

def new_db_connection():

    try:

        connection = mysql.connector.connect(
            user='jbroeren',
            password='Hello123!!*',
            host='localhost',
            database='restdb'
        )

        if connection.is_connected():
            print('Connected to MySQL database')

    except Error as e:
        print(e)


    if connection is not None and connection.is_connected():
        return connection