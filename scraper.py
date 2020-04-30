# IMPORTS

import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
from scraperNgp import oneScrap as oneScrap


# WRITING TO THE FIRESTORE

cred = credentials.Certificate("../keys/digital-curator-firebase-adminsdk-h28c6-a4ddaed626.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'digital-curator.appspot.com'
})

db = firestore.client()

def writeArtwork(key, artwork):
    doc_ref = db.collection(u'artworks').document(key)
    doc_ref.set(artwork)

bucket = storage.bucket()

def saveImage(key, imagePath):
    blob = bucket.blob(key)
    outfile = imagePath
    blob.upload_from_filename(outfile)

# GENERAL SETTINGS

outputName = input('Jak pojmenujeme výstup: ')

# CREATING DIRECTORY

path = 'collections/' + outputName

try:
    os.mkdir(path)
except OSError:
    print("Creation of the directory %s failed" % path)
else:
    print("Successfully created the directory %s " % path)


# NATIONAL GALLERY IN PRAGUE

subcollectionId = input('Vložte signaturu sbírky (Př: CZE:NG.Vp_): ') or 'CZE:NG.Vp_'
startUrlNumber = int(input('Vložte číslo prvního díla ke stažení: ') or 10)
endUrlNumber = int(input('Vložte číslo posledního díla ke stažení: ') or 20)

def scrapNgp(subcollectionId, startUrlNumber, endUrlNumber, outputName):

    # SETTING INPUTS

    webUrl = 'http://sbirky.ngprague.cz'
    collectionUrl = webUrl + '/dielo/' + subcollectionId

    # STARTING CYCLE

    while startUrlNumber < endUrlNumber:
        startUrlNumber += 1
        pageUrl = str(collectionUrl) + str(startUrlNumber)
        print('Searching at: ' + str(pageUrl)+ ' ...')
        artwork = oneScrap(pageUrl, webUrl, outputName)

        # IF CONTAINS ARTWORK CALLS FUNCTIONS FOR WRITING TO THE FIRESTORE AND SAVING IMAGE TO THE STORAGE

        if not artwork == None:
            writeArtwork(artwork['Key'], artwork)
            saveImage(artwork['Key'], path + '/' + artwork['Image ID'])

scrapNgp(subcollectionId, startUrlNumber, endUrlNumber, outputName)

# WRITING RESUME

artworks = db.collection(u'artworks').stream()
artworksCount = 0
for artwork in artworks:
    artworksCount += 1

print('Scrapping successful! Digital Curator database now contains ' + str(artworksCount) + ' artworks.')





