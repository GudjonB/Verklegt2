from bs4 import BeautifulSoup as bs
import urllib.request
conn = psycopg2.connect(dsn)
cur = conn.cursor()

class PropertyInfo:
    def __init__(self, name, price, evaluation, type, size, rooms, description, age, location, imgs):
        self._name = name
        self._price = price
        self._evaluation = evaluation
        self._type = type
        self._size = size
        self._rooms = rooms
        self._description = description
        self._age = age
        self._imgs = imgs

    def printAll(self):
        print("Name: " + self._name)
        print("Price: " + self._price)
        print("Evaluated price: " + self._evaluation)
        print("Type: " + self._type)
        print("Size: " + self._size)
        print("Rooms: " + self._rooms)
        print("Description: " + self._description)
        print("Year built: " + self._age)
        print("Photos: ")
        for img in self._imgs:
            print(img)


properties = []
page = urllib.request.urlopen('https://www.mbl.is/fasteignir/leit/?q=80f323c5382397611e72800316f250d1')
parse = bs(page, "lxml")
links = []
for i in parse.findAll("div", {"class": "realestate-head"}):
    for a in i.findAll("a", href=True):
        links.append("https://www.mbl.is" + a['href'])

for link in links:
    page = urllib.request.urlopen(link)
    parse = bs(page, "lxml")
    counter = 1
    tempName = ""
    tempPrice = ""
    tempEval = ""
    tempType = ""
    tempSize = ""
    tempRooms = ""
    tempDescr = ""
    tempAge = ""
    tempLocation = ""
    tempImgs = []
    for i in parse.findAll("div", {"class": "realestate-infobox"}):
        # print(i)
        for td in i.findAll("td", {"class": "value"}):
            if counter == 1:
                tempPrice = (td.text).strip()
            elif counter == 2:
                tempEval = (td.text).strip()
            elif counter == 5:
                tempType = (td.text).strip()
            elif counter == 6:
                tempAge = (td.text).strip()
            elif counter == 7:
                tempSize = (td.text).strip()
            elif counter == 8:
                tempRooms = (td.text).strip()
            counter += 1

        for desc in i.findAll("div", {"class": "description"}):
            tempDescr = (desc.text).split('window.')[0].strip()

    for prop in parse.findAll("div", {"class": "realestate"}):
        for name in prop.findAll("span", {"class": "realestate-headline-address"}):
            tempName = (name.text).split('  ')[0].strip()
            tempLocation = (name.text).split('  ')[5].strip()

    for imgTags in parse.findAll("div", {"class": "item"}):
        for img in imgTags.findAll("img", {"src": True}):
            tempImgs.append(img['src'])

    propertyInstance = PropertyInfo(tempName, tempPrice, tempEval, tempType, tempSize, tempRooms, tempDescr, tempAge,
                                    tempLocation, tempImgs)
    properties.append(propertyInstance)

properties[0].printAll()  # skipta út 0 fyrir ehv tölu frá 1-24
