import asyncio
import time
from db import *
from language import NER, nerPerformer

cnx = startconnection()

# Create a queue that we will use to store our "workload".
queueTasks = asyncio.Queue()

# this script asynchronously uploads videos and checks for vids every 10 secs.
async def newSentenceCheck():

    getsentencecursor = cnx.cursor()
    getsessioncursor = cnx.cursor()

    while True:

        print("check for new sentences")

        # add stuff to queue in endless loop
        getsentencecursor.execute(rewritequery("SELECT * FROM sentence WHERE status=%s"), (0, ))

        for sentence in getsentencecursor.fetchall():
            print("sentence found")
            resultsentence = dict(zip([column[0] for column in getsentencecursor.description], sentence))

            getsessioncursor.execute(rewritequery("SELECT * FROM sessions WHERE id=%s"), (resultsentence["session_id"], ))

            resultsession = dict(zip([column[0] for column in getsessioncursor.description], getsessioncursor.fetchone()))

            data = (resultsentence, resultsession)

            await queueTasks.put(data)

            # getsentencecursor.execute(rewritequery("UPDATE sentences SET status=%s WHERE id=%s"), (1, resultsentence["id"]))
            cnx.commit()

        # wait till next run
        await asyncio.sleep(10)

async def sentenceProcessor():

    # generate class for models before entering loop
    models = NER().nermodels

    while True:

        print("checking for stuff")

        await asyncio.sleep(1)

        # if queue is empty wait a second till next task check
        if queueTasks.empty():
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, time.sleep, 1)

        # Get a "work item" out of the queue.
        data = await queueTasks.get()

        (resultsentence, resultsession) = data

        # depending on modeltype do stuff with the data
        processdata = models[resultsession["language"]]

        result = nerPerformer(processdata, resultsentence["sentence"])

        # mark task as done
        queueTasks.task_done()


async def main():
    feed_data = asyncio.create_task(newSentenceCheck())
    process_data = asyncio.create_task(sentenceProcessor())
    await asyncio.gather(feed_data, process_data)

while True:
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()