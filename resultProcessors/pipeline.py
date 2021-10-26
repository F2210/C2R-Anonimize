import string

def clean(text):
    replacelist = string.punctuation
    for sign in replacelist:
        text = text.replace(sign, "")
    return text

def findEntity(resultdict, start, sentencewordid, entity, sentencedict):
    notFound = True
    index = start
    while notFound:
        if index in sentencewordid:
            notFound = False
        elif index == -1:
            break
        else:
            index -= 1
    resultdict[sentencedict[index]] = entity["entity"]

    return resultdict

def resultProcessor(text, result):

        text = clean(text)

        sentencedict = {}
        sentencelength = 0
        for word in text.split(" "):
            sentencedict[sentencelength] = word
            sentencelength += len(word) + 1

        sentencewordid = sentencedict.keys()

        resultdict = {}

        try:
            end = result[0]["end"]
            counter = 0
            for entity in result[1:]:
                start = entity["start"]
                if end == start:
                    resultdict = findEntity(resultdict, start, sentencewordid, entity, sentencedict)
                    counter += 1
                elif counter == 0:
                    resultdict = findEntity(resultdict, start, sentencewordid, entity, sentencedict)
                else:
                    counter = 0
                    end = entity["start"]
        except:
            pass

        return resultdict