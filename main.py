# IMPORTS

import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
from scraperNgp import ngpScrap
from scraperMgb import mgbScrap
from scraperPcg import pcgScrap
from scraperBmv import bmvScrap


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

def scrapNgp():

    # SETTING INPUTS

    subcollectionId = input('Insert subcollection signature (Ex: CZE:NG.O_): ') or 'CZE:NG.O_'
    startUrlNumber = int(input('Insert first ID for scrapping: ') or 10)
    endUrlNumber = int(input('Insert last ID for scrapping: ') or 20)
    webUrl = 'http://sbirky.ngprague.cz'
    collectionUrl = webUrl + '/dielo/' + subcollectionId

    # STARTING CYCLE

    while startUrlNumber < endUrlNumber:
        startUrlNumber += 1
        pageUrl = str(collectionUrl) + str(startUrlNumber)
        print('Searching at: ' + str(pageUrl)+ ' ...')
        artwork = ngpScrap(pageUrl, webUrl)

        # IF CONTAINS ARTWORK CALLS FUNCTIONS FOR WRITING TO THE FIRESTORE AND SAVING IMAGE TO THE STORAGE

        if not artwork == None:
            writeArtwork(artwork['Key'], artwork)
            saveImage('artworks/' + artwork['Key'], 'temp/' + artwork['Image ID'])
            os.remove('temp/' + artwork['Image ID'])


# MORAVIAN GALLERY IN BRNO

def scrapMgb():

    # SETTING INPUTS
    
    subcollectionId = input('Insert subcollection signature (Ex: CZE:MG.A_): ') or 'CZE:MG.A_'
    startUrlNumber = int(input('Insert first ID for scrapping: ') or 1)
    endUrlNumber = int(input('Insert last ID for scrapping: ') or 20)
    webUrl = 'http://sbirky.moravska-galerie.cz'
    collectionUrl = webUrl + '/dielo/' + subcollectionId

    # STARTING LOOP

    while startUrlNumber < endUrlNumber:
        startUrlNumber += 1
        pageUrl = str(collectionUrl) + str(startUrlNumber)
        print('Searching at: ' + str(pageUrl)+ ' ...')
        artwork = mgbScrap(pageUrl, webUrl)

        # IF ARTWORK CONTAINS IMAGE IT CALLS FUNCTIONS FOR WRITING TO THE FIRESTORE AND SAVING IMAGE TO THE STORAGE

        if not artwork == None and 'Image ID' in artwork:
            writeArtwork(artwork['Key'], artwork)
            saveImage('artworks/' + artwork['Key'], 'temp/' + artwork['Image ID'])
            os.remove('temp/' + artwork['Image ID'])

# PRAGUE CITY GALLERY

def scrapPcg():

    # SETTING INPUTS

    subcollectionId = input('Insert subcollection signature (Ex: CZK:US.K-): ') or 'CZK:US.K-'
    startUrlNumber = int(input('Insert first ID for scrapping: ') or 1)
    endUrlNumber = int(input('Insert last ID for scrapping: ') or 20)
    webUrl = 'http://ghmp.cz'
    collectionUrl = webUrl + '/online-sbirky/detail/' + subcollectionId

    # STARTING LOOP

    while startUrlNumber < endUrlNumber:
        startUrlNumber += 1
        pageUrl = str(collectionUrl) + str(startUrlNumber)
        print('Searching at: ' + str(pageUrl)+ ' ...')
        artwork = pcgScrap(pageUrl, webUrl)

        # IF ARTWORK CONTAINS IMAGE IT CALLS FUNCTIONS FOR WRITING TO THE FIRESTORE AND SAVING IMAGE TO THE STORAGE

        if not artwork == None and 'Image ID' in artwork:
            writeArtwork(artwork['Key'], artwork)
            saveImage('artworks/' + artwork['Key'], 'temp/' + artwork['Image ID'])
            os.remove('temp/' + artwork['Image ID'])

# PRAGUE CITY GALLERY

def scrapBmv():

    # SETTING INPUTS

    startUrlNumber = int(input('Insert first ID for scrapping: ') or 1)
    endUrlNumber = int(input('Insert last ID for scrapping: ') or 20)
    webUrl = 'https://sammlung.belvedere.at'
    collectionUrl = webUrl + '/objects/'

    # STARTING LOOP

    while startUrlNumber < endUrlNumber:
        startUrlNumber += 1
        pageUrl = str(collectionUrl) + str(startUrlNumber)
        print('Searching at: ' + str(pageUrl) + ' ...')
        artwork = bmvScrap(pageUrl, webUrl)

        # IF ARTWORK CONTAINS IMAGE IT CALLS FUNCTIONS FOR WRITING TO THE FIRESTORE AND SAVING IMAGE TO THE STORAGE

        if not artwork == None and 'Image ID' in artwork:
            writeArtwork(artwork['Key'], artwork)
            saveImage('artworks/' + artwork['Key'], 'temp/' + artwork['Image ID'])
            os.remove('temp/' + artwork['Image ID'])


scrapBmv()


# WRITING RESUME

artworks = db.collection(u'artworks').stream()
artworksCount = 0
for artwork in artworks:
    artworksCount += 1

print('[Curator]: Scrapping successful! Digital Curator database now contains ' + str(artworksCount) + ' artworks.')





