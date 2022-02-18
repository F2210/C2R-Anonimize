import string

def clean(text):
    replacelist = string.punctuation
    for sign in replacelist:
        text = text.replace(sign, "")
    return text

def findEntity(resultdict, text, entity):

    startofword = entity["start"]

    text = text[startofword:]
    word = text.split(" ")[0].replace(",", "")

    label = entity["entity"]

    if "PER".lower() in label.lower():
        resultdict[word] = "PER"

    return resultdict

def resultProcessor(text, results):

    resultdict = {}

    print(results)

    for entity in results:
        resultdict = findEntity(resultdict, text, entity)

    return resultdict