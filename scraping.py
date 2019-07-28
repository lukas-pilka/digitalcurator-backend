from requests_html import HTMLSession
import urllib.request
session = HTMLSession()
import csv
import os

# SETTING INPUTS

scrapedWebsite = 'http://sbirky.ngprague.cz'
collectionSignature = input('Vložte signaturu sbírky (Př: CZE:NG.Vp_): ')
startUrlNumber = int(input('Vložte číslo prvního díla ke stažení: '))
endUrlNumber = int(input('Vložte číslo posledního díla ke stažení: '))
outputName = input('Jak pojmenujeme výstup: ')

collectionURL = scrapedWebsite + '/dielo/' + collectionSignature
outputNameCsv = 'collections/' + outputName + '-items.csv'

# DOWNLOAD IMAGE

path = 'collections/' + outputName

try:
    os.mkdir(path)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)

# DOWNLOAD IMAGE

def dlJpg(iiUrl, filePath, ngInventoryId):
    fullPath = 'collections/' + filePath + ngInventoryId + '.jpg'
    urllib.request.urlretrieve(iiUrl, fullPath)

# STARTING CYCLE

def scraping(startUrlNumber, endUrlNumber):

    while startUrlNumber < endUrlNumber:
        startUrlNumber += 1
        scrapedUrl = str(collectionURL) + str(startUrlNumber)
        ng = session.get(scrapedUrl)

        # IF FINDS ITEML NAME, IT CONTINUES

        ngItemName = ng.html.find('.nadpis-dielo', first=True)

        if not ngItemName == None:

            print(scrapedUrl)

            # SCRAPING SELECTION

            # SCRAPPING ITEM NAME

            ngItemName = ng.html.find('.nadpis-dielo', first=True)
            if not ngItemName == None:
                ngItemName = ngItemName.text
            else:
                ngItemName = 'nezadáno'
            print(ngItemName)

            # SCRAPPING AUTHOR

            ngAuthor = ng.html.find('.inline', first=True)
            if not ngAuthor == None:
                ngAuthor = ngAuthor.text
            else:
                ngAuthor = 'nezadáno'
            print(ngAuthor)

            # SCRAPPING CREATION DATE

            ngCreationDate = ng.html.find('tr', containing='datace:', first=True)
            if not ngCreationDate == None:
                ngCreationDate = ''.join(list(ngCreationDate.text)[8:]) # CUT X LETTERS FROM BEGINNING
            else:
                ngCreationDate = 'nezadáno'
            print(ngCreationDate)

            # SCRAPPING SIZES

            ngSizes = ng.html.find('tr', containing='rozměry:', first=True)
            if not ngSizes == None:
                ngSizes = ''.join(list(ngSizes.text)[9:]) # CUT X LETTERS FROM BEGINNING
            else:
                ngSizes = 'nezadáno'
            print(ngSizes)

            # SCRAPPING TOPIC UNITS

            ngTopicUnits = ng.html.find('tr', containing='tematické celky:', first=True)
            if not ngTopicUnits == None:
                ngTopicUnits = ''.join(list(ngTopicUnits.text)[17:]) # CUT X LETTERS FROM BEGINNING
            else:
                ngTopicUnits = 'nezadáno'
            print(ngTopicUnits)

            # SCRAPPING MATERIAL

            ngMaterial = ng.html.find('tr', containing='materiál:', first=True)
            if not ngMaterial == None:
                ngMaterial = ''.join(list(ngMaterial.text)[10:]) # CUT X LETTERS FROM BEGINNING
            else:
                ngMaterial = 'nezadáno'
            print(ngMaterial)

            # SCRAPPING TECHNIQUE

            ngTechnique = ng.html.find('tr', containing='technika:', first=True)
            if not ngTechnique == None:
                ngTechnique = ''.join(list(ngTechnique.text)[10:]) # CUT X LETTERS FROM BEGINNING
            else:
                ngTechnique = 'nezadáno'
            print(ngTechnique)

            # SCRAPPING MARKING

            ngMarking = ng.html.find('tr', containing='značení:', first=True)
            if not ngMarking == None:
                ngMarking = ''.join(list(ngMarking.text)[9:]) # CUT X LETTERS FROM BEGINNING
            else:
                ngMarking = 'nezadáno'
            print(ngMarking)

            # SCRAPPING INVENTORY NUMBER

            ngInventoryId = ng.html.find('tr', containing='inventární číslo:', first=True)
            if not ngInventoryId == None:
                ngInventoryId = ''.join(list(ngInventoryId.text)[18:]) # CUT X LETTERS FROM BEGINNING
                ngInventoryId = ngInventoryId.replace(" ", "-")
            else:
                ngInventoryId = 'nezadáno'
            print(ngInventoryId)

            # SCRAPPING COLLECTION

            ngCollection = ng.html.find('tr', containing='sbírka:', first=True)
            if not ngCollection == None:
                ngCollection = ''.join(list(ngCollection.text)[8:]) # CUT X LETTERS FROM BEGINNING
            else:
                ngCollection = 'nezadáno'
            print(ngCollection)

            # SCRAPPING LICENCE

            ngLicence = ng.html.find('tr', containing='licence:', first=True)
            if not ngLicence == None:
                ngLicence = ''.join(list(ngLicence.text)[9:]) # CUT X LETTERS FROM BEGINNING
            else:
                ngLicence = 'nezadáno'
            print(ngLicence)

            # SCRAPPING DESCRIPTION

            ngDescription = ng.html.find('.description', first=True)
            if not ngDescription == None:
                ngDescription = ngDescription.text
            else:
                ngDescription = 'nezadáno'
            print(ngDescription)

            # SCRAPPING IMAGE

            iiUrl = ng.html.find('.img-dielo', first=True)
            if not iiUrl == None:
                iiUrl = iiUrl.attrs
                iiUrl = iiUrl.get("src")  # TAKES VALUE OF SRC ATTRIBUTE IN DICTIONARY
                iiUrl = scrapedWebsite + iiUrl
                dlJpg(iiUrl, outputName + '/', ngInventoryId)

            else:
                iiUrl = 'bez obrázku'
            print(iiUrl)

            # WRITING CSV ROW
            csvHeader = ['Název díla, Autor, Vytvořeno, Rozměry, Tématické celky, Materiál, Značení, Inventární číslo, Sbírka, Licence, Popis']
            itemRow = [ngItemName, ngAuthor, ngCreationDate, ngSizes, ngTopicUnits, ngMaterial, ngMarking, ngInventoryId, ngCollection, ngLicence, ngDescription]

            with open(outputNameCsv, 'a') as csvFile:
                writer = csv.writer(csvFile)
                # writer.writerow(csvHeader)
                writer.writerow(itemRow)

            csvFile.close()

        else:
            print(startUrlNumber)

# CALL SCRAPING FUNCTION WITH START AND ENDING URL NUMBER

scraping(startUrlNumber, endUrlNumber)