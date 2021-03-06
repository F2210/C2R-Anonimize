import datetime, requests
from time import sleep


primersesh = requests.post("http://192.168.1.175:8001/sessiondata?type=open",
                      json={"sessionID": str(datetime.datetime.now().timestamp() + 4)}).json()["response_data"]["ID"]


def main():

    try:
        requests.post(
            "http://192.168.1.175:8001/textdedata",
            json={
                "text": "---ignore---",
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
    sleep(2)