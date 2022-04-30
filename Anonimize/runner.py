import sys, os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from Anonimize.db import new_db_connection
from Anonimize.controller import de_identify

def main():

    connection = new_db_connection()

    with connection.cursor() as c:
        c.execute(
            'SELECT * FROM REST_textdata WHERE status=0',
        )

        results = [dict(zip([column[0] for column in c.description], i)) for i in c.fetchall()]

    for result in results:

        with connection.cursor() as c:
            c.execute(
                'UPDATE REST_textdata SET status=1 WHERE status=0',
            )
            connection.commit()

        with connection.cursor() as c:
            c.execute(
                'SELECT * FROM REST_session WHERE id=%s',
                [result["session_id"]]
            )

            session = dict(zip([column[0] for column in c.description], c.fetchone()))

        textdata = {
            "id": result["id"],
            "original_text": result["original_text"],
            "sessionid": result["session_id"],
        }

        session = {
            "id": result["session_id"],
            "language": session["language"]
        }

        # print("starting processing")
        process = de_identify(textdata, session)
        process.daemon = True
        process.start()

    connection.close()