import psycopg2
import sqlite3

LOCAL = True

def rewritequery(query):
    if LOCAL:
        return query.replace("%s", "(?)")
    else:
        return query

def startconnection():
    if LOCAL:
        cnx = sqlite3.connect(database="./localdatabase")

    else:
        cnx = psycopg2.connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            dbname=POSTGRES_TABLE
        )

    return cnx