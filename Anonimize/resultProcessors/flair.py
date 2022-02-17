
def resultProcessor(text, results):

    returnresults = {}

    print(results)

    for result in results:
        result = result.to_dict()

        label = result["labels"][0].value

        if "I" in label:
            print(label)
        elif "B" in label:
            print(label)

        if "PER" in label:
            returnresults[result["text"]] = "PER"

    return returnresults