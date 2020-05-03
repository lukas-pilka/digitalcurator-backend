import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

# ML LABELS API

def detect_labels_uri(uri):
    """Detects labels in the file located in Google Cloud Storage or on the
    Web."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.label_detection(image=image)
    labels = response.label_annotations
    labelsDict = {}

    for label in labels:
        labelsDict[label.description] = label.score

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return labelsDict


# ACCESSING TO THE FIRESTORE

cred = credentials.Certificate("../keys/digital-curator-f02e06005c99.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
artworks = db.collection(u'artworks').stream()

def writeArtwork(key, artwork):
    doc_ref = db.collection(u'artworks').document(key)
    doc_ref.set(artwork)

# CALLING CLOUD VISION API

for artwork in artworks: # Checking Firebase items
    artworkDict = artwork.to_dict() # Converts Firestore document to dictionary
    imageUrl = 'https://storage.googleapis.com/digital-curator.appspot.com/artworks/' + artworkDict['Key'] # Generates Image Url
    print('\n[Curator]: I received: ' + artworkDict['Key'] + ': ' + artworkDict['Title'] +', ' + imageUrl)
    if not 'ML Labels' in artworkDict:
        try:
            artworkDict['ML Labels'] = detect_labels_uri(imageUrl) # Calling AI Labeling function and updating dictionary
            writeArtwork(artworkDict['Key'], artworkDict) # Writing updated dictionary to firestore
            print('[Curator]: Nice artwork! I think that it is: ' + str(artworkDict['ML Labels']))
        except:
            print('[Curator]: I can not find image on this url.')
    else:
        print('[Curator]: ML Labels already exists. I keep the original labels.')




