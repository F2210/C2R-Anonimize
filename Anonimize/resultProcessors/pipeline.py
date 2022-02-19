import string

def clean(text):
    replacelist = string.punctuation
    for sign in replacelist:
        text = text.replace(sign, "")
    return text

def findEntity(resultdict, text, entity):

    startofword = entity["start"]

    endofword = entity["end"]

    word = text[startofword:endofword].replace(",", "")

    label = entity["entity"]

    if "PER".lower() in label.lower():
        resultdict[word] = "PER"

    return resultdict

def resultProcessor(text, results):

    resultdict = {}

    entityset = []

    processedresults = []
    for entity in results[::-1]:

        if "I" in entity["entity"]:
            entityset.append(entity)

        if "B" in entity["entity"]:

            endslice = entityset[0]["end"] if len(entityset) > 0 else entity["end"]

            char = text[endslice]
            while char != " " or char != "." or char != ",":
                try:
                    char = text[endslice]
                except IndexError:
                    char = " "
                endslice += 1

            print("yeeehaw")

            endslice -= 1
            entityset = []

            processedresults.append({
                "start": entity["start"],
                "end": endslice,
                "entity": "PER",
                "length": len(entityset) + 1
            })

    for entity in processedresults:

        resultdict = findEntity(resultdict, text, entity)

    return resultdict