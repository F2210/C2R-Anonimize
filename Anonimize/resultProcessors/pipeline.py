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

    resultdict[word] = "PER"

    return resultdict

def resultProcessor(text, results):

    text = text + " "

    resultdict = {}

    entityset = []

    print("processing results")
    processedresults = []

    print(results)

    for entity in results[::-1]:

        if "I" in entity["entity"]:
            entityset.append(entity)

        if "B" in entity["entity"]:

            endslice = entityset[0]["end"] if len(entityset) > 0 else entity["end"]

            # if endslice > len(text):
            #     print("------------")
            #     endslice = len(text) - 1
            #     char = text[endslice]
            #     print(char)
            #     endslice = len(text)
            #     char = text[endslice]
            #     print(char)
            #     print("------------")
            # else:
            #     char = text[endslice]

            notFound = True
            while notFound:
                char = text[endslice]
                if char == " " or char in string.punctuation:
                    notFound = False
                endslice += 1

            print("yeeehaw")

            endslice -= 1
            entityset = []

            if "PER".lower() in entity["entity"].lower():

                processedresults.append({
                    "start": entity["start"],
                    "end": endslice,
                    "entity": "PER",
                    "length": len(entityset) + 1
                })

    resultdict = {}
    if processedresults != []:
        for entity in processedresults:
            print("finding: ", entity)
            resultdict = findEntity(resultdict, text, entity)

    print("processed results")
    return resultdict