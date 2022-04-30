import sys, os
from pathlib import Path

from time import sleep

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from Anonimize.db import new_db_connection
from Anonimize.controller import de_identify

connection = new_db_connection()

def syllable_count(sentence):
    count = 0
    vowels = "aeiouy"
    for word in sentence.split(" "):
        if word != "":
            if word[0] in vowels:
                count += 1
            for index in range(1, len(word)):
                if word[index] in vowels and word[index - 1] not in vowels:
                    count += 1
                    if word.endswith("e"):
                        count -= 1
            if count == 0:
                count += 1
    return count

def main():

    if not connection.is_connected():
        exit()

    with connection.cursor() as c:
        c.execute(
            'SELECT * FROM REST_textdata WHERE status=0',
        )

        results = [dict(zip([column[0] for column in c.description], i)) for i in c.fetchall()]

    print(results)

    for result in results:

        with connection.cursor() as c:
            c.execute(
                'UPDATE REST_textdata SET status=1 WHERE id=%s',
                [result["session_id"]]
            )
            connection.commit()

        try:
            with connection.cursor() as c:
                c.execute(
                    'SELECT * FROM REST_session WHERE id=%s',
                    [result["session_id"]]
                )

                session = dict(zip([column[0] for column in c.description], c.fetchone()))

            # if syllable_count(result["original_text"]) < 12:


            textdata = {
                "id": result["id"],
                "original_text": result["original_text"],
                "sessionid": result["session_id"],
            }

            session = {
                "id": result["session_id"],
                "language": session["language"]
            }

            print("starting processing")
            process = de_identify(textdata, session)
            process.daemon = True
            process.start()

        except:
            with connection.cursor() as c:
                c.execute(
                    'UPDATE REST_textdata SET status=0 WHERE id=%s',
                    [result["session_id"]]
                )
                connection.commit()

    connection.close()

while True:
    main()
    sleep(0.5)