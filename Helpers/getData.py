from bs4 import BeautifulSoup as bs
import urllib.request

properties = []
page = urllib.request.urlopen('https://www.mbl.is/fasteignir/leit/?q=80f323c5382397611e72800316f250d1')
parse = bs(page, "lxml")
links = []
zips = []
for i in parse.findAll("div", {"class": "realestate-head"}):
    for a in i.findAll("a", href=True):
        links.append("https://www.mbl.is" + a['href'])
        zips.append((a.text).split(",")[1].split(" ")[0])

for link in links:
    page = urllib.request.urlopen(link)
    parse = bs(page, "lxml")
    counter = 1
    zipCounter = 0
    imgCounter = 0
    tempAddress = ""
    tempSize = 0
    tempRooms = 0
    tempBathrooms = ""
    tempPrice = ""
    tempCategory = ""

    tempDescr = ""
    tempYearBuilt = ""
    tempLocation = ""
    tempImgs = []
    file = open("populate.sql", "a")
    for i in parse.findAll("div", {"class": "realestate-infobox"}):
        # print(i)
        for td in i.findAll("td", {"class": "value"}):
            if counter == 2:
                tempPrice = (td.text).strip()
            elif counter == 5:
                tempCategory = (td.text).strip()
            elif counter == 6:
                tempYearBuilt = (td.text).strip()
            elif counter == 7:
                tempSize = (td.text).split(" ")[0].strip()
            elif counter == 8:
                tempRooms = (td.text).strip()
            elif counter == 11:
                tempBathrooms = (td.text).strip()
            counter += 1

        for desc in i.findAll("div", {"class": "description"}):
            tempDescr = (desc.text).split('window.')[0].strip()

    for prop in parse.findAll("div", {"class": "realestate"}):
        for name in prop.findAll("span", {"class": "realestate-headline-address"}):
            tempAddress = (name.text).split('  ')[0].strip()
            tempLocation = (name.text).split('  ')[5].strip()

    for imgTags in parse.findAll("div", {"class": "item"}):
        for img in imgTags.findAll("img", {"src": True}):
            tempImgs.append(img['src'])


    file.write("INSERT INTO " + "Properties(address, size, rooms, bathrooms,"
    " yearBuilt, price)" + " VALUES (" + "\"" + str(tempAddress) + "\", "
    + str(tempSize) + ", " + str(tempRooms) + ", " + str(tempBathrooms) + ", "
    + str(tempYearBuilt) + ", " + "\"" + str(tempPrice) + "\");\n")


    #file.write("INSERT INTO " + "Description(description) VALUES (\"" + str(tempDescr) +
    #"\");\n")

    zipCounter += 1
#properties[0].printAll()  # skipta út 0 fyrir ehv tölu frá 1-24
