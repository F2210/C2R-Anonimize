import datetime, requests
from time import sleep


def main():

    primersesh = requests.post("http://192.168.1.175:8001/sessiondata?type=open",
                          json={"sessionID": str(datetime.datetime.now().timestamp() + 4)}).json()["response_data"]["ID"]

    try:
        requests.post(
            "http://192.168.1.175:8001/textdedata",
            json={
                "text": "Dit primer tekst.",
                "sessionID": primersesh
            },
            timeout=0.000000001)

    except requests.exceptions.ReadTimeout:
        pass
    except requests.exceptions.ConnectTimeout:
        pass
    except requests.exceptions.ConnectionError:
        pass

while True:
    main()
    print("priming")
    sleep(10)