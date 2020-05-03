# IMPORTS

import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
from scraperNgp import oneScrap as oneScrap


# WRITING TO THE FIRESTORE

cred = credentials.Certificate("../keys/digital-curator-f02e06005c99.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'digital-curator.appspot.com'
})

db = firestore.client()

def writeArtwork(key, artwork):
    doc_ref = db.collection(u'artworks').document(key)
    doc_ref.set(artwork, merge=True)

bucket = storage.bucket()

def saveImage(key, imagePath):
    blob = bucket.blob(key)
    outfile = imagePath
    blob.upload_from_filename(outfile)

# NATIONAL GALLERY IN PRAGUE

subcollectionId = input('Insert subcollection signature (Ex: CZE:NG.O_): ') or 'CZE:NG.O_'
startUrlNumber = int(input('Insert first ID for scrapping: ') or 10)
endUrlNumber = int(input('Insert last ID for scrapping: ') or 20)

def scrapNgp(subcollectionId, startUrlNumber, endUrlNumber):

    # SETTING INPUTS

    webUrl = 'http://sbirky.ngprague.cz'
    collectionUrl = webUrl + '/dielo/' + subcollectionId

    # STARTING CYCLE

    while startUrlNumber < endUrlNumber:
        startUrlNumber += 1
        pageUrl = str(collectionUrl) + str(startUrlNumber)
        print('Searching at: ' + str(pageUrl)+ ' ...')
        artwork = oneScrap(pageUrl, webUrl)

        # IF CONTAINS ARTWORK CALLS FUNCTIONS FOR WRITING TO THE FIRESTORE AND SAVING IMAGE TO THE STORAGE

        if not artwork == None:
            writeArtwork(artwork['Key'], artwork)
            saveImage('artworks/' + artwork['Key'], 'temp/' + artwork['Image ID'])
            os.remove('temp/' + artwork['Image ID'])

scrapNgp(subcollectionId, startUrlNumber, endUrlNumber)

# WRITING RESUME

artworks = db.collection(u'artworks').stream()
artworksCount = 0
for artwork in artworks:
    artworksCount += 1

print('[Curator]: Scrapping successful! Digital Curator database now contains ' + str(artworksCount) + ' artworks.')





