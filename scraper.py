import os

# GENERAL SETTINGS

outputName = input('Jak pojmenujeme výstup: ')

# Creating directory

path = 'collections/' + outputName

try:
    os.mkdir(path)
except OSError:
    print("Creation of the directory %s failed" % path)
else:
    print("Successfully created the directory %s " % path)


# NATIONAL GALLERY IN PRAGUE

from scraperNgp import oneScrap as oneScrap

collectionSignature = input('Vložte signaturu sbírky (Př: CZE:NG.Vp_): ') or 'CZE:NG.Vp_'
startUrlNumber = int(input('Vložte číslo prvního díla ke stažení: ') or 10)
endUrlNumber = int(input('Vložte číslo posledního díla ke stažení: ') or 20)

def scrapNgp(collectionSignature, startUrlNumber, endUrlNumber, outputName):

    # SETTING INPUTS

    webUrl = 'http://sbirky.ngprague.cz'
    collectionUrl = webUrl + '/dielo/' + collectionSignature
    outputNameCsv = 'collections/' + outputName + '-items.csv'

    # STARTING CYCLE

    while startUrlNumber < endUrlNumber:
        startUrlNumber += 1
        pageUrl = str(collectionUrl) + str(startUrlNumber)
        print('Searching at: ' + str(pageUrl)+ ' ...')
        print(oneScrap(pageUrl, webUrl, outputNameCsv, outputName))

scrapNgp(collectionSignature, startUrlNumber, endUrlNumber, outputName)

