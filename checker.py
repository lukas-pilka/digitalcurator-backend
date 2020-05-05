import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

# WRITING TO THE FIRESTORE

cred = credentials.Certificate("../keys/digital-curator-f02e06005c99.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'digital-curator.appspot.com'
})

db = firestore.client()
artworksNgp = db.collection(u'artworks').where('Collection', '==', 'National Gallery in Prague').stream()
artworksMgb = db.collection(u'artworks').where('Collection', '==', 'Moravian Gallery in Brno').stream()
artworksPcg = db.collection(u'artworks').where('Collection', '==', 'Prague City Gallery').stream()
bucket = storage.bucket()

print("Bucket {} connected.".format(bucket.name))

# COUNTING ITEMS

def dbCounter(artworks):
    print('counting Firebase objects...')
    objectCounter = 0
    labelCounter = 0
    for artwork in artworks: # Checking Firebase items
        objectCounter += 1
        artworkDict = artwork.to_dict()  # Converts Firestore document to dictionary
        if 'ML Labels' in artworkDict:
            labelCounter += 1
    result = {'Objects': objectCounter, 'Objects with Labels': labelCounter}
    return result

def filesCounter():
    print('counting Cloud Storage images...')
    counter = 0
    for artwork in bucket.list_blobs(prefix='artworks'): # Checking Firebase storage
        counter += 1
    return counter



print('National Gallery in Prague' + str(dbCounter(artworksNgp)))
print('Moravian Gallery in Brno' + str(dbCounter(artworksMgb)))
print('Prague City Gallery' + str(dbCounter(artworksPcg)))

print("Storage contains {} images.".format(filesCounter()))
