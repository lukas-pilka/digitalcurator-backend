from requests_html import HTMLSession
import urllib.request
session = HTMLSession()
import csv
import os

# SETTING INPUTS

scrapedWebsite = 'https://digital.belvedere.at/objects/'
startUrlNumber = int(input('Vložte číslo prvního díla ke stažení: '))
endUrlNumber = int(input('Vložte číslo posledního díla ke stažení: '))
outputName = input('Jak pojmenujeme výstup: ')

# DOWNLOAD IMAGE

path = 'collections/' + outputName

try:
    os.mkdir(path)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)

# DOWNLOAD IMAGE

def dlJpg(iiUrl, filePath, InventoryId):
    fullPath = 'collections/' + str(filePath) + str(InventoryId) + '.jpg'
    urllib.request.urlretrieve(iiUrl, fullPath)

# STARTING CYCLE

def scraping(startUrlNumber, endUrlNumber):

    while startUrlNumber < endUrlNumber:
        startUrlNumber += 1
        scrapedUrl = scrapedWebsite + str(startUrlNumber)
        scraping = session.get(scrapedUrl)

        # IF FINDS ITEML NAME, IT CONTINUES

        ItemName = scraping.html.find('.detail-item-details', first=True)

        if not ItemName == None:

            # print(scrapedUrl)

            # SCRAPING SELECTION

            # SCRAPPING INVENTORY NUMBER

            inventoryId = scraping.html.find('.invnoField .detailFieldValue', first=True)
            if not inventoryId == None:
                inventoryId = inventoryId.text
            else:
                inventoryId = 'not set'

            # SCRAPPING IMAGE

            iiUrl = scraping.html.find('.width-img-wrap img', first=True)
            if not iiUrl == None:
                iiUrl = iiUrl.attrs
                iiUrl = iiUrl.get("src")  # TAKES VALUE OF SRC ATTRIBUTE IN DICTIONARY
                iiUrl = 'https://digital.belvedere.at' + str(iiUrl)
                dlJpg(iiUrl, outputName + '/', inventoryId)
                print('Downloading item ' + inventoryId + ' from ' + iiUrl)
            else:
                print('no image')

        else:
            print('Nothing at: ' + str(startUrlNumber))

# CALL SCRAPING FUNCTION WITH START AND ENDING URL NUMBER

scraping(startUrlNumber, endUrlNumber)