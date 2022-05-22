import datetime
import random, requests, time
import asyncio

conv1 = "Hoi Ik ben Jacco. Hoi aangenaam, Ik ben dr Vreeswijk, Wat kan ik voor je doen. Ik heb last van mijn scheenbeen. Ik heb 1 grote rode plek en ik weet niet echt wat het is. Oké, Laten we dan eens gaan kijken waar je last van hebt, meneer Broeren. Als je even naar de behandeltafel wandelt en daar gaat zitten, kijken ik even. Oké, Dit is inderdaad een rode plek. Doet het pijn als ik hier duw. Klein beetje het zeurt wat. En Als ik hier duw. Ja dat doet pijn. Oké ga er maar weer zitten. U heeft een onderhuids ontsteking. Mocht die groter worden, of als u last van koorts krijgt, dan moet u even bellen en dan moeten we even opnieuw kijken. Misschien moet u dan antibiotica. Maar vooralsnog nog ziet het er goed uit. Omcirkel de plek die rood is en doe dat dan over 24 uur nog een keer. Als het dan dus groter is geworden, dan mag u even contact opnemen.".split(".")

conv2 = "Goedemorgen. Goedemorgen. Ik ben Jan, hoi. Hoi, Ik ben dokter De boer. Wat kan ik voor u doen. Ik heb last van mijn oor. Oké, dan gaan we even kijken. gaat u maar op de behandeltafel zitten, dan pak ik even mijn oor kijkapparaat erbij. Nou oké, Het is rood van binnen. Heeft u koorts. Nee, Ik heb geen koorts alleen oorpijn. En is er vocht uit de oor komen lopen Meneer De Vries. Nee, dat heb ik nog niet gemerkt. Vorige keer was het wel zo. Nou en wanneer was de vorige keer. Hmmm. Ongeveer een week geleden. Oh, Dat is heel snel op deze keer. Hoeveel pijn deed hij toen. Nou, Ik heb toen een paracetamolletje genomen om in slaap te vallen. Oké. En heeft u nu iets geslikt. Nee maar ik zat daar wel over na te denken. O. Nou, u heeft gewoon een ontsteking op het moment, maar Omdat u het een week hiervoor ook al had, lijkt het niet zo goed weg te gaan. Dus ga ik u op een antibiotica kuur zetten. Oké, ik maak even een verwijsbriefje voor u. Uw naam was. Jan De Vries. Oké, krijgt u een verwijsbrief mee namens dr. Piet de boer. Oké, dank u wel, dan ga ik nu even langs de apotheek.".split(".")

conv3 = "Sevilla Het was echt fucking chill. Het was mooi weer, heel veel koffie drinken, was echt chill. En ja dus ook heel veel getraind, want we waren op trainingskamp. 17 keer in 10 dagen hebben we volgens mij getraind. Heel veel, was ook wel goed te doen aan het eind. Nog veel tapas gegeten. Ja, We hebben heel veel tapas gegeten. Maar met dat vele trainingen kreeg je geen last van je rug Jacco. Op de 4/5 dag wel last van mijn rug, maar max, dat trok ook wel weer weg. Toen hebben we volgens mij 20 km training iets korter moeten varen, maar ja, Dat was op zich ook niet zo'n probleem, want we trainden sowieso al super veel. En, Het was echt super chill. Dat Malte op een motorboot zat, hij coachte echt. Dat was heel Nice. En, je hebt daar dus coach boten die varen dan achter je boot aan. En, daar staat dan je coach op. Dus die kan dan eigenlijk heel erg goed om je heen varen om te kijken wat je fout doet. Dat helpt enorm met coaching en ze kunnen ook heel Nice filmen, dus je hebt gewoon de hele tijd filmpjes van de zij voor en achterkant waar je heel goed kan zien wat je zelf ook fout doet. En Dat is een stuk makkelijker om dingen te verbeteren die je coach dan benoemd. Omdat je het in één keer zelf ziet. Hoe verbleven jullie daar. We zaten in het huisje daar met 9 of 8. Volgens mij. Er was nog wat gezeik, omdat er twee perse met elkaar in een kamer wilden, zodat ze niet met andere Mensen In de Kamer hoefden. Maar uiteindelijk was het wel opgelost en was nog heel gezellig. Was wel een kleine keuken, dus koken was vrij ingewikkeld. En de ruimte was sowieso zelf niet heel erg groot, dus ja, Het was wat krap soms. Maar op zich was dat ook allemaal geen ramp. En, Het was wel heel gezellig en We hadden ook allemaal fietsen. We hadden allemaal fietsen die we konden gebruiken om van het huisje naar de baan te gaan, want Dat is toch wel een goed halfuur lopen Als je het te voet moest doen. En die fietsen, die kocht je dan eigenlijk over van een lokale fietsenmaker daar voor € 100 ofzo. En dan bracht je die aan het eind van de dag terug aan het eind van de week. En dan betalen ze je gewoon € 70, terug, of de helft in ieder geval. En dat. Nou ja, dat bedrag krijg je dan gewoon terug en dan betaal je dus effectief veel minder dan wanneer je een fiets huurt voor de hele week. Alleen op de eerste twee dagen hadden we nog geen fiets. In sevilla hebben ze dus allemaal stepjes. Een step die je kan gebruiken. En dan betaal je na gebruik. Alleen € 1 per minuut ofzo. Dus Dat is best wel veel, maar Als je niet heel lang onderweg bent. Oh nee, 20 cent per minuut. We hadden trouwens al onze spullen in de boot gestopt. Daardoor had je niet dat je ook nog een ruimbagage tas mee moest nemen, omdat je gewoon je kleding In de boot stopt. En, die kan je dan daarna daar ook weer er uit halen. Dus Dat is. Ja, je hoeft niet kleren niet allemaal In het vliegtuig mee te nemen. Wat ook chill is. Dus Dat was de trip naar Sevilla.".split(".")

conv4 = "Goedemiddag, Hallo dokter Horstman. Waarom ben je hier. Nou, Ik heb een klein ongelukje gehad met een pan met pasta. OK vertel, wat is er gebeurd. Ik was op zaterdagmiddag pasta aan het koken voor na een roeiwedstrijd. En Ja, toen liep ik met een pan met heet water van het fornuis naar de grote steen om pasta af te gieten en toen brak de linker pannen hendel af. En ja toen kreeg ik al het hele kokende water over mijn bovenbeen heen. Dus Dat is vrij jammer. Oké, en wat heb je toen gedaan. Heb je toen direct gekoeld. Ja, Ik heb toen eerst een half uur koud lauw water over de wond heen Laten lopen. En toen ben ik daarna naar de huisartsenpost gegaan bij het diak en daar hebben ze toen naar de wond gekeken. Het verbonden. En nou ja. Toen is er paraffine gaas overheen gelegd en nog wat niet klevend, ander gaas wat niet ingevet was. En daar bovenop dan gewoon verband. Maar ja, Het was paasweekend, dus ik kon ook niet langsgaan bij de apotheek om dat verband te verwisselen, dus. Nee, Daarom moest ik ook hierlangs nog en van de huisarts post moest ik sowieso nog langs voor een controle. Omdat ze gewoon wilden dat er nu nog naar gekeken werd. Dus ja. Oké, dan ga ik even kijken naar je been. Ik ga eventjes het verband eraf halen. Is het heel gevoelig. Ja, oké. Nou, Als ik er zo naar kijk, dan ziet het er goed uit. Ik zie geen ontstekingen. Het ruikt ook niet ontstoken, dus Dat is goed. Ik wil nog even kijken of je wel goed gevoel hebt In de hele wond. Dus ik pak even een wattenstaafje om te kijken. Met wie ging je roeien dit weekend. Ik roeide met Wouter in een dubbel op de voorjaars regatta, maar ja, daar kon ik niet meer op starten op zondag met deze wond, helaas. Dat was een beetje jammer. De race ging wel heel goed op zaterdag. We zijn er nu algemeen derde in het klassement, dus Dat is wel nice. Voel je dit. Ja. En dit. Ja ook goed, oké, dan is het gevoel in ieder geval goed, dan gaan we er nu zalf op smeren. Deze zalf die doodt bacteriën om ontstekingen te voorkomen. En daaroverheen, doen we dan hetzelfde. Paraffine gaas zoals dat ze bij de huisartsenpost hebben gedaan en nog wat ander gaas en dan. Krijg je waarschijnlijk een elastisch verband daar weer overheen, wat zorgt dat het verband niet af gaat zakken. Met al dat vet ertussen gebeurt het nogal snel. Weet je toevallig welke huisarts je had gezien In het diak. Ja, huisarts van der Mark. Oké. Dan ga ik even de update van hem in jouw medisch dossier bekijken wat hij er ook van vond. Maar ik vind het dus goed uitzien, mag je over twee dagen terugkomen voor controle. En dan kijken we even hoe je wond zich ontwikkelt. Ik wil vooral heel goed In de gaten houden dat het niet gaat ontsteken, dus op het moment dat je koorts krijgt of een een geelgroene afzetting op de wond ziet, dan mag je onmiddellijk naar de huisartsenpost bellen. Want dan moeten we daar gelijk naar kijken. Maar voor nu ziet het er heel goed uit, dus ik wens je vooral veel sterkte. Neem ook goede pijnstilling, je mag gewoon maximale hoeveelheid slikken, dus Dat is. 400 mg Ibuprofen en 1000 mg paracetamol. En dat kan je gewoon net zo lang slikken totdat de pijn afneemt, maar je bent gezond, dus ik vermoed dat het herstel relatief snel gaat. Ik denk dat je over ongeveer 1,5 week wel weer zou moeten kunnen lopen en roeien. Oké, dank u wel. Tot ziens en tot morgen dan. Ja. Tot volgende keer, joe. Beterschap.".split(".")

nersentence = """
En hoe lang heeft u daar al last van meneer de Vries. Weet u dat.
Omdat Pieter toen een tijdje bij het UMC Utrecht heeft gelopen om te onderzoeken hoe dat kwam. Want hij is autospuiter geweest en daar heeft hij klachten van.
Nou net iemand die dronken is. Concentratieproblemen ja. Want dan zei De Jonge vaak van, ja dat heb ik toch net verteld.
Ben als huisschilder begonnen. En dat bedrijf, schildersbedrijf De Groot BV, liet me later ook constructie schilderen en dat is echt heel vies werk.
Ja, en ik laat Henk weleens pinnen met dat ik erbij ben.
En hebben jullie dan ook huishoudelijke hulp daarnaast of doet Angela eigenlijk alles zelf of.
Die zegt: wil je even met me meegaan naar de Albert Heijn. Dat soort dingen vind ik leuk om te doen.
Mijn dochter, Fatima, ja, die helpt mij bijvoorbeeld als ik bij haar ga lopen.
Nou, Yara de Roon waar ze het over heeft is de oudste van het gezin.
Meneer en mevrouw Postma, onze buren, gaan weleens mee naar de Ikea.
En dat moet ik ook eigenlijk bij de Cito doen want ik werk ook al een jaar of tien bij de Cito. Ik maak examens voor mijn eigen vak. Dat doen we met de Cito groep.
Dit is wel de derde hond, maar met die andere twee had ie niet zoveel. Maar dit is zijn hondje, Boris.
Nee, hetzelfde huis aan de Marco Rijkersstraat.
Mijn zus is dan ook zelf lerares op de Klimop. Die is heel, ja, Eva weet wel hoe ze die dingen aan moet pakken.
Ik woon uitstekend in Amsterdam-Zuidoost.
Toen zei je tegen mij weet je nou toch waar ik was. Kennedylaan.
Toen ben ik nog in het Sint Jansdal geweest, samen met meneer Meyer.
Ja, Ik ben nou vanaf de Antoni van Leeuwenhoekweg gelopen. Ik weet niet of je weet waar de Antoni van Leeuwenhoekstraat is.
Ik pak dan bijvoorbeeld de trein naar Amersfoort Vathorst. Dat is hier om de hoek.
Dat heb ik van de kant van mijn moeder, de familie van der Meulen.
Ik heb vier achterkleinkinderen: Zoë, Marijn, Levi en Danique.
toen ik in deze flat ging wonen vijftien jaar terug vroeg arts Bram van den Bosch van praktijk Zeist, of ik een trap in het huis heb. Altijd doen zei meneer van den Bosch toen.
En toen zei ik nou ik begin maar met de gemeente. Dat is de gemeente Cuijk. Of nee, gemeente Beers was het toen nog.
Is tweeënnegentig geworden. Was ook een Hendriks, dus een zus van mijn vader.
"""


# convo = conv1 + conv2 + conv3 + conv4

# print(len(convo))
print("starting")

sesh1 = requests.post("http://192.168.1.175:8001/sessiondata?type=open",
                          json={"sessionID": str(datetime.datetime.now().timestamp() + 1)}).json()["response_data"][
        "ID"]
sesh2 = requests.post("http://192.168.1.175:8001/sessiondata?type=open",
                          json={"sessionID": str(datetime.datetime.now().timestamp() + 2)}).json()["response_data"][
        "ID"]
sesh3 = requests.post("http://192.168.1.175:8001/sessiondata?type=open",
                          json={"sessionID": str(datetime.datetime.now().timestamp() + 3)}).json()["response_data"][
        "ID"]

sesh4 = requests.post("http://192.168.1.175:8001/sessiondata?type=open",
                          json={"sessionID": str(datetime.datetime.now().timestamp() + 4)}).json()["response_data"][
        "ID"]

counter = 0

convos = [conv1, conv2, conv3, conv4]
seshs = [sesh1, sesh2, sesh3, sesh4]

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

    sesh4 = requests.post("http://192.168.1.175:8001/sessiondata?type=open",
                          json={"sessionID": str(datetime.datetime.now().timestamp() + 4)}).json()["response_data"][
        "ID"]

    convos = [conv1, conv2, conv3, conv4]
    seshs = [sesh1, sesh2, sesh3, sesh4]

    errorcount = 0
    sentencecount = 0
    while True:
        for conv in range(0, 4):

            try:
                try:
                    requests.post(
                        "http://192.168.1.175:8001/textdedata",
                        json={
                            "text": convos[conv][sentencecount],
                            "sessionID": seshs[conv]
                        },
                        timeout=0.000000000000000001)
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

def syllable_count(sentence):
    count = 0
    vowels = "aeiouy"
    for word in sentence.split(" "):
        if word != "":
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

# syllables = 0
# for conv in convo:
#     for word in conv.split(" "):
#         if word != "":
#             syllables += syllable_count(word)

# print(syllables)


def testerNER():

    sesh4 = requests.post("http://192.168.1.175:8001/sessiondata?type=open",
                          json={"sessionID": str(datetime.datetime.now().timestamp() + 4)}).json()["response_data"][
        "ID"]

    # print("nertest", sesh4)

    for sentence in nersentence.split("\n"):

        requests.post(
            "http://192.168.1.175:8001/textdedata",
            json={
                "text": sentence,
                "sessionID": sesh4
            },
            timeout=5)

    time.sleep(5)

async def sender(sentence, sessionid):
    requests.post(
        "http://192.168.1.175:8001/textdedata",
        json={
            "text": sentence,
            "sessionID": sessionid
        },
        timeout=10)



def testerBULK():

    for conv in range(0, 4):
        convo = convos[conv]

        print("bulktest: ", seshs[conv])
        print("start", datetime.datetime.now().timestamp())

        for sentence in convo:

            asyncio.run(sender(sentence.strip(), seshs[conv]))

            syllables = syllable_count(sentence)
            time.sleep(syllables / 6.3)


        time.sleep(30)


def hypoTester():

    conv = [
        "Tom",
        "Hallo mijn naam is Tom",
        "Hallo mijn naam is Tom en ik roei iedere dag",
        "Hallo mijn naam is Tom en ik roei iedere dag op mijn favoriete roeivereniging Triton"
    ]


    for i in range(0, len(conv)):

        sesh = requests.post("http://192.168.1.175:8001/sessiondata?type=open",
                              json={"sessionID": str(datetime.datetime.now().timestamp() + 4)}).json()["response_data"][
            "ID"]

        for j in range(0, 30):

                sentence = conv[i]

                asyncio.run(sender(sentence.strip(), sesh))

                syllables = syllable_count(sentence)
                time.sleep(syllables / 6.3)

        time.sleep(30)


def testerSingleSentence():

    sesh4 = requests.post("http://192.168.1.175:8001/sessiondata?type=open",
                          json={"sessionID": str(datetime.datetime.now().timestamp() + 4)}).json()["response_data"][
        "ID"]

    print(sesh4)
    print(datetime.datetime.now().timestamp())

    count = 0

    try:
        requests.post(
            "http://192.168.1. "
            ":8001/textdedata",
            json={
                "text": "Dat Malte op een motorboot zat, hij coachte echt goed op zeer specifieke punten.",
                "sessionID": sesh4
            },
            timeout=5)

    except requests.exceptions.ReadTimeout:
        pass
    except requests.exceptions.ConnectTimeout:
        pass

    syllables = syllable_count("Dat Malte op een motorboot zat, hij coachte echt goed op zeer specifieke punten.")

    seccount = syllables / 8
    count += 1
    time.sleep(seccount)

print("starting")
# testerConvo()
hypoTester()

# testerSingleSentence()
# time.sleep(120)
# testerSingleSentence()
# time.sleep(120)
# testerSingleSentence()
# time.sleep(120)
# testerSingleSentence()
# time.sleep(120)
# testerSingleSentence()
# time.sleep(120)
# testerSingleSentence()
# time.sleep(120)
# testerSingleSentence()
# time.sleep(120)
# testerSingleSentence()
# time.sleep(120)
# testerSingleSentence()
# time.sleep(120)


# print("end", datetime.datetime.now().timestamp())
# time.sleep(360)
# testerNER()
# print("finished")
