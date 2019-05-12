from bs4 import BeautifulSoup as bs
import urllib.request
import csv

def clearFiles():
    f1 = open('zip.csv', "w+") #open with write permission to clear file
    f1.close()
    f2 = open('categories.csv', "w+")
    f2.close()
    f3 = open('properties.csv', "w+")
    f3.close()
    f4 = open('propertyImgs.csv', "w+")
    f4.close()
    f5 = open('description.csv', "w+")
    f5.close()

def getPropertyLinksAndZips():
    page = urllib.request.urlopen('https://www.mbl.is/fasteignir/leit/?page=11&q=80f323c5382397611e72800316f250d1') #page to get links from
    parse = bs(page, "lxml")                                                                                #parse the html from the link
    links = []
    zips = []
    for i in parse.findAll("div", {"class": "realestate-head"}):
        for a in i.findAll("a", href=True):                                     #find every a-tag with a href
            links.append("https://www.mbl.is" + a['href'])                      #store the links in an array
            zips.append((a.text).split(",")[1].split(" ")[0].split('\n')[1])    #store the zips in an array
    return links, zips

def writeToCsv():
    # declare the variables that will be written to the csv
    #properties.csv
    tempAddress = ""
    tempSize = 0
    tempRooms = 0
    tempBathrooms = 0
    tempPrice = 0
    tempYearBuilt = ""
    tempLocation = ""
    #categories.csv
    tempCategory = ""
    #description.csv
    tempDescr = ""
    #propertyImgs.csv
    tempImgs = []

    links, zips = getPropertyLinksAndZips()
    for link in links:                      #for each property
        page = urllib.request.urlopen(link) #open page
        parse = bs(page, "lxml")            #parse html
        counter = 1                         #counter for each property attribute

        for i in parse.findAll("div", {"class": "realestate-infobox"}):     #go to the infobox
            for td in i.findAll("td", {"class": "value"}):                  #look at the values of the attributes
                if counter == 1:                                            #first attribute is the sales price
                    tempRealPrice = (td.text).strip()                       #if format is 'Tilboð'
                    if tempRealPrice == 'Tilboð':
                        tempRealPrice = 0
                    elif "." in tempRealPrice:                                #if format is 'xx.xxx.xxx kr'
                        tempRealPrice = ((td.text).split(".")[0]            #remove dots from string
                                         + (td.text).split(".")[1]
                                         + (td.text).split(".")[2]).strip()
                        tempRealPrice = tempRealPrice.split(" ")[0]         #remove 'kr' from string
                if counter == 2:                                            #second attribute is evaluated price
                    tempPrice = (td.text).strip()                           #remove 'kr' from string
                    if tempPrice.count(".") > 2:                                    #if format is 'xx.xxx.xxx kr'
                        tempPrice = ((td.text).split(".")[0]                #remove dots from string
                                     + (td.text).split(".")[1]
                                     + (td.text).split(".")[2])
                    tempPrice = tempPrice.split(" ")[0]
                    if int(tempPrice) == 0:             #if price is still zero use sales price
                        tempPrice = tempRealPrice
                elif counter == 5:                      #the fifth attribute is the category
                    tempCategory = (td.text).strip()
                    if tempCategory == 'Fjölbýli':      #translate most common categories
                        tempCategory = 'Apartment building'
                    elif tempCategory == 'Par/Raðhús':
                        tempCategory = 'Town House'
                    elif tempCategory == 'Einbýli':
                        tempCategory = 'Villa'
                    elif tempCategory == 'Hæðir':
                        tempCategory = 'Multiple floors'
                elif counter == 6:                      #6th attribute is year built
                    tempYearBuilt = (td.text).strip()
                    if str(tempYearBuilt) == 'None':    #if no year built is determined use default
                        tempYearBuilt = 2000
                elif counter == 7:                                                 #7th attribute is size
                    tempSize = int((td.text).split(" ")[0].split(".")[0].strip())  #cut out the "m^2" and "."
                elif counter == 8:                      #8th attribute is rooms
                    tempRooms = (td.text).strip()
                    if tempRooms == 'Óuppgefið':
                        tempRooms = 0
                elif counter == 11:                     #11th attribute is bathrooms
                    tempBathrooms = (td.text).strip()
                    if tempBathrooms == 'Óuppgefið':
                        tempBathrooms = 0
                counter += 1


            for desc in i.findAll("div", {"class": "description"}):     #get description
                tempDescr = (desc.text).split('window.')[0].strip()

        for prop in parse.findAll("div", {"class": "realestate"}):
            for name in prop.findAll("span", {"class": "realestate-headline-address"}): #get address and city from headline
                tempAddress = (name.text).split('  ')[0].strip()
                tempLocation = (name.text).split('  ')[5].strip()
                if tempLocation == '':
                    tempLocation = (name.text).split('  ')[6].strip()

        for imgTags in parse.findAll("div", {"class": "item"}): #get image links
            for img in imgTags.findAll("img", {"src": True}):
                tempImgs.append(img['src'])

        #write to csv
        with open('zip.csv', 'a') as f1:
            writer = csv.writer(f1, delimiter=',', lineterminator='\n', )
            row = [zips[0], tempLocation]
            zips.pop(0)
            writer.writerow(row)
        with open('categories.csv', 'a') as f2:
            writer = csv.writer(f2, delimiter=',', lineterminator='\n', )
            row = [tempCategory]
            writer.writerow(row)
        with open('properties.csv', 'a') as f3:
            writer = csv.writer(f3, delimiter=',', lineterminator='\n', )
            row = [tempAddress, tempSize, tempRooms, tempBathrooms, tempYearBuilt, tempPrice]
            writer.writerow(row)
        with open('propertyImgs.csv', 'a') as f4:
            writer = csv.writer(f4, delimiter=',', lineterminator='\n', )
            n = 0
            for img in tempImgs:
                row = [tempPrice, img]
                writer.writerow(row)
                n += 1
                if n == 3:
                    break
        with open('description.csv', 'a', encoding="utf-8") as f5:
            writer = csv.writer(f5, delimiter=',', lineterminator='\n', )
            row = [tempDescr]
            writer.writerow(row)



def readFromCsv(filename):
    retData = []
    if filename == 'description.csv':
        with open(filename, 'r', encoding="utf-8") as f:
            writer = csv.reader(f)
            for row in writer:
                retData.append(row)
    else:
        with open(filename, 'r') as f:
            writer = csv.reader(f)
            for row in writer:
                retData.append(row)
    return retData

def downloadImgs(data):
    j = 0
    for i in range(len(data)):
        nameCounter = 1
        while nameCounter != 4:
            urllib.request.urlretrieve(data[j-1][1],'../Properties/Images/' + data[j-1][0] + '_mynd_' + str(nameCounter) + '.png')
            nameCounter += 1
        j += 1

