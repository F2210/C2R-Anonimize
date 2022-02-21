import datetime
import random, requests, time


conv1 = "Hoi Hoi Hoi Ik ben Jacco. Hoi aangenaam, Ik ben dr Vreeswijk. Wat kan ik voor je doen? Maar ja, hoi, Ik heb last van mijn scheenbeen. Ik weet eigenlijk 1 grote rode plek en Ik weet niet echt wat het is. Oké, Laten we dan eens gaan kijken waar je last van heeft, meneer Broeren. Elk team naar de wandeling tafel gaat hij daar maar zitten, kijken ik even? Oké, Dit is inderdaad een rode plek. Doet het pijn Als ik hier duw? Klein beetje het zeurt wat. En Als ik hier duw? Ja dat doet pijn. Oké ga er maar weer zitten. U heeft een onderhuids ontsteking. Mocht die groter worden, of als u last van koorts krijgt, dan moet u even de huisarts weer bellen en dan. Moeten we even opnieuw kijken? Misschien moet u dan antibiotica? Maar volgens nog? Ziet er goed uit. Omcirkelde plek die je rood is en doe dat dan over 24 uur. Nog een keer moment dat het dan dus groter is geworden. Dan mag u even contact opnemen. Oke bedankt. Tot ziens. Tot ziens.".split(".")

conv2 = "Goedemorgen goedemorgen, Ik ben Jan, hoi, hoi, Ik ben dokter De boer. Wat kan ik voor u doen? Hé? Ja, Ik heb last van mijn oor. Oké, dan gaan we even kijken, gaat hij maar op de behandeltafel zitten, pak ik even mijn. Oorkijk apparaat erbij. Nou oké, Het is rood van binnen. Heeft u koorts? Nee, Ik heb geen koord Alleen oorpijn. En is er vocht uit de oor komen lopen Meneer De Vries? Nee, dat heb ik nog niet gemerkt. Vorige keer was het wel zo. Nou en wanneer was de vorige keer? Hmmm. Ongeveer een week geleden? Oh, Dat is heel snel op deze keer. Hoeveel pijn deed hij toen? Nou, Ik heb toen een paracetamolletje genomen om in slaap te vallen. Oké. En nu heeft hij nu iets geslikt? Nee maar een. Ik zat daar weer over na te denken. O. Nou, u heeft gewoon een ontsteking op het moment, maar Omdat u het een week hiervoor ook al had, lijkt het niet zo goed weg te gaan. Dus ga ik u op een antibiotica kuur zetten. Oké, ik zal het even verwijsbriefje voor u. Uw naam was. Jan De Vries. Oké, krijgt hij een verwijsbrief mee namens dr. Piet de boer. Oké, dank u wel, dan ga ik nu even langs de apotheek. Tot ziens tot de volgende keer doeg.".split(".")

conv3 = "Sevilla Het was echt fucking chill. Ik mooi weer dat koffie drinken dan echt chill. En ja dus ook heel veel getraind, want er waren op trainingskamp nog veer. Was het. 17 keer in 10 dagen hebben we volgens mij getraind. Heel veel was ook wel goed doen aan het eind. En ja, We hebben eigenlijk heel veel tapas ge tijd. Op de 4/5 dag wel last van mijn rug. Is, toen hebben we volgens mij 20 km training iets korter moeten varen, maar ja, Dat was op zich ook niet zo'n probleem, want de trainer is sowieso al super veel. En, Het was echt super chill. Dat motor was coach, hij coachte echt, zie ik goed. Dat was heel Nice. En, Het is daar je daar dus coach boten die varen dan achter je achter je boot aan. En, daar staat dan je coach op. Dus die kan dan eigenlijk heel erg goed om je heen vragen om te kijken wat er wat je fout doet. Dat helpt enorm met coaching en ze kunnen ook heel Nice filmen, dus je hebt gewoon de hele tijd filmpjes van de zijde voor de achterkant waar je heel goed kan zien wat je zelf ook fout doet. En Dat is een stuk makkelijker om dingen te verbeteren die je coach dan benoemd. Omdat je het in één keer zelf ziet. We zaten met een met het huisje daar met 9 of 8. Volgens mij. Er was nog wat gezeik Omdat er twee die wilde perse met elkaar in een Kamer, zodat ze niet met andere Mensen In de Kamer hoefden. Maar uiteindelijk was het wel opgelost en was nog heel gezellig. Was wel een kleine keuken, dus koken was vrij ingewikkeld. En de ruimte was sowieso zelf niet heel erg groot, dus ja, Het was wat krap soms. Maar op zich was dat ook allemaal geen ramp. En, Het was wel heel gezellig en We hebben ook allemaal fietsen. We hadden allemaal fietsen die we konden gebruiken om van het huisje naar de baan te gaan, want Dat is toch wel een goed halfuur lopen Als je het goed Als je te voet moest doen. En die fietsen, die kocht je dan eigenlijk over van een lokale fietsenmaker daar voor € 100 ofzo. En dan krijg je bracht je die aan het eind van de dag terug aan het eind van de week. En dan betalen ze je gewoon was het € 70, terug weer of de helft in ieder geval. En dat. Nou ja, dat bedrag krijg je dan gewoon terug en dan betaal je dus effectief veel minder dan wanneer je een fiets huur voor de hele week. Alleen op de eerste twee dagen hadden we nog geen fiets. Seizoen Huurde stepjes hebben daar een. Een step die je kan gebruiken? En dan betaal je pas het? Alleen € 1 per minuut ofzo. Dus Dat is best wel veel, maar Als je niet heel lang onderweg bent, maar nee, 20 cent per per minuut. Nou zeg trouwens heel kort, veel minder geld. Is dat wel zo prima? En wat ook wel nis was dat we de kleding In de boot konden stoppen, dus. Daardoor had je niet dat je ook nog een ruimbagage tas mee moest nemen Omdat je gewoon je kleding In de boot stopt. En, die kan je dan daar naar daar ook weer uithalen. Dus Dat is. Ja, je hoeft niet kleren niet allemaal In het vliegtuig mee te nemen. Wat ook fucking chill is. Dus Dat was de trip naar s 4.".split(".")

nersentence = """
En hoe lang heeft u daar al last van meneer de Vries? Weet u dat?
Omdat Pieter toen een tijdje bij het UMC Utrecht heeft gelopen om te onderzoeken hoe dat kwam. Want hij is autospuiter geweest en daar heeft hij klachten van.
Nou net iemand die dronken is. Concentratieproblemen ja. Want dan zei De Jonge vaak van, ja dat heb ik toch net verteld?
Ben als huisschilder begonnen. En dat bedrijf, schildersbedrijf De Groot BV, liet me later ook constructie schilderen en dat is echt heel vies werk.
Ja, en ik laat Henk weleens pinnen met dat ik erbij ben.
En hebben jullie dan ook huishoudelijke hulp daarnaast of doet Angela eigenlijk alles zelf of?
Die zegt: wil je even met me meegaan naar de Albert Heijn? Dat soort dingen vind ik leuk om te doen.
Mijn dochter, Fatima, ja, die helpt mij bijvoorbeeld als ik bij haar ga lopen.
Nou, Yara de Roon waar ze het over heeft is de oudste van het gezin.
Meneer en mevrouw Postma, onze buren, gaan weleens mee naar de Ikea.
En dat moet ik ook eigenlijk bij de Cito doen want ik werk ook al een jaar of tien bij de Cito. Ik maak examens voor mijn eigen vak. Dat doen we met de Cito groep.
Dit is wel de derde hond, maar met die andere twee had ie niet zoveel. Maar dit is zijn hondje, Boris.
Nee, hetzelfde huis aan de Marco Rijkersstraat.
Mijn zus is dan ook zelf lerares op de Klimop. Die is heel, ja, Eva weet wel hoe ze die dingen aan moet pakken.
Ik woon uitstekend in Amsterdam-Zuidoost.
Toen zei je tegen mij weet je nou toch waar ik was? Kennedylaan.
Toen ben ik nog in het Sint Jansdal geweest, samen met meneer Meyer.
Ja, Ik ben nou vanaf de Antoni van Leeuwenhoekweg gelopen. Ik weet niet of je weet waar de Antoni van Leeuwenhoekstraat is?
Ik pak dan bijvoorbeeld de trein naar Amersfoort Vathorst. Dat is hier om de hoek.
Dat heb ik van de kant van mijn moeder, de familie van der Meulen.
Ik heb vier achterkleinkinderen: Zoë, Marijn, Levi en Danique.
toen ik in deze flat ging wonen vijftien jaar terug vroeg arts Bram van den Bosch van praktijk Zeist, of ik een trap in het huis heb. Altijd doen zei meneer van den Bosch toen.
En toen zei ik nou ik begin maar met de gemeente. Dat is de gemeente Cuijk. Of nee, gemeente Beers was het toen nog.
Is tweeënnegentig geworden. Was ook een Hendriks, dus een zus van mijn vader.
"""


convo = conv1 + conv2 + conv3

print(len(convo))

counter = 0

def testerConvo():
    sesh1 = requests.post("http://192.168.1.175:8001/sessiondata?type=open",
                          json={"sessionID": str(datetime.datetime.now().timestamp() + 1)}).json()["response_data"][
        "ID"]
    sesh2 = requests.post("http://192.168.1.175:8001/sessiondata?type=open",
                          json={"sessionID": str(datetime.datetime.now().timestamp() + 2)}).json()["response_data"][
        "ID"]
    sesh3 = requests.post("http://192.168.1.175:8001/sessiondata?type=open",
                          json={"sessionID": str(datetime.datetime.now().timestamp() + 3)}).json()["response_data"][
        "ID"]

    convos = [conv1, conv2, conv3]
    seshs = [sesh1, sesh2, sesh3]

    print("convotest", str(seshs))

    errorcount = 0
    sentencecount = 0
    while True:
        for conv in range(0, 3):

            try:
                try:
                    requests.post(
                        "http://192.168.1.175:8001/textdedata",
                        json={
                            "text": convos[conv][sentencecount],
                            "sessionID": seshs[conv]
                        },
                        timeout=5)
                except requests.exceptions.ConnectTimeout:
                    pass
                except requests.exceptions.ReadTimeout:
                    pass

            except IndexError:
                errorcount += 1
                pass

            if errorcount == 3:
                return ""

            if conv == 2:
                sentencecount += 1
                time.sleep(2)
                errorcount = 0

def syllable_count(word):
    count = 0
    vowels = "aeiouy"
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

syllables = 0
for conv in convo:
    for word in conv.split(" "):
        if word != "":
            syllables += syllable_count(word)

print(syllables)


def testerNER():

    sesh4 = requests.post("http://192.168.1.175:8001/sessiondata?type=open",
                          json={"sessionID": str(datetime.datetime.now().timestamp() + 4)}).json()["response_data"][
        "ID"]

    print("nertest", sesh4)

    for sentence in nersentence.split("\n"):

        requests.post(
            "http://192.168.1.175:8001/textdedata",
            json={
                "text": sentence,
                "sessionID": sesh4
            },
            timeout=5)

def testerBULK():

    sesh4 = requests.post("http://192.168.1.175:8001/sessiondata?type=open",
                          json={"sessionID": str(datetime.datetime.now().timestamp() + 4)}).json()["response_data"][
        "ID"]

    print("bulktest: ", sesh4)

    for sentence in convo:

        requests.post(
            "http://192.168.1.175:8001/textdedata",
            json={
                "text": sentence,
                "sessionID": sesh4
            },
            timeout=5)

print("starting")
testerConvo()
time.sleep(360)
testerBULK()
time.sleep(360)
testerNER()
print("finished")



