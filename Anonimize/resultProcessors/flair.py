
def resultProcessor(text, results):

    returnresults = {}

    for result in results:
        result = result.to_dict()

        label = result["labels"][0].value

        if "PER" in label:
            resultlabel = "PER"
        elif "ORG" in label:
            resultlabel = "ORG"
        elif "LOC" in label:
            resultlabel = "LOC"
        elif "MISC" in label:
            resultlabel = "MISC"

        returnresults[result["text"]] = resultlabel

    return returnresults