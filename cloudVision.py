import os
import pymongo
import io
from PIL import Image

# Basics
collectionLocalDirectory = 'collections/sbirka-grafiky'

# Connecting MongoDB

client = pymongo.MongoClient("mongodb+srv://lukaspilka:Apollo11@digitalcurator-hw3um.mongodb.net/test?retryWrites=true&w=majority")
mydb = client["artpieces"]
mycol = mydb["items"]

# Google Auth

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/lukaspilka/digitalcurator-247310-b5388c78514e.json"

# Asking Google for objects

def localize_objects(path):

    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    responses = []

    for object_ in objects:
        vertices = []
        for vertex in object_.bounding_poly.normalized_vertices:
            vertices.append({"x": vertex.x, "y": vertex.y})
        responses.append({
            "mid": object_.mid,
            "name": object_.name,
            "score": object_.score,
            "boundingPoly": {
                "normalizedVertices": vertices
            }
        })

    return responses

# Checks objects on local imagws and writes results to MongoDB

def getObjects(counter):
    print('Startuji rozpoznávání objektů')
    for filename in os.listdir(collectionLocalDirectory):

        # Gets inventory ID

        ngInventoryId = str(filename)
        ngInventoryId = ngInventoryId[:-4]

        # Asking MonogoDB if item exists

        item = mycol.find_one({"ngInventoryId": ngInventoryId})
        if not item:
            print(ngInventoryId + ': položka neexistuje v MongoDB')
            continue

        if 'localizedObjectAnnotations' in item:
            print(ngInventoryId + ': položka existuje v MongoDB, ale je již rozpoznána')
            continue

        # Creates img path
        imagePath = collectionLocalDirectory + '/' + filename
        print(imagePath)

        # Saving Results from Google

        result = localize_objects(imagePath)
        print(ngInventoryId + ': položka existuje v MongoDB a dosud nebyla rozpoznána. Zapisuji: ' + str(result))

        # Writing to MonogoDB

        myquery = {"ngInventoryId": ngInventoryId}
        newvalues = {"$set": {"localizedObjectAnnotations": result}}
        mycol.update_one(myquery, newvalues)

        # breaking counter
        if counter == maxTasks:
            break

        counter += 1

# Asking Google for faces

def detect_faces(path, iWidth, iHeight):

    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    responses = []

    for face in faces:
        formatedVertices = []
        for vertex in face.bounding_poly.vertices:
            formatedVertices.append({"x": vertex.x / iWidth, "y": vertex.y / iHeight})
        responses.append({
            "anger": likelihood_name[face.anger_likelihood],
            "joy": likelihood_name[face.joy_likelihood],
            "surprise": likelihood_name[face.surprise_likelihood],
            "boundingPoly": {
                "vertices": formatedVertices
            }
        })

    return responses

# Checks faces on local images and writes results to MongoDB

def getFaces(counter):
    print('Startuji rozpoznávání tváří')
    for filename in os.listdir(collectionLocalDirectory):
        # Gets inventory ID

        ngInventoryId = str(filename)
        ngInventoryId = ngInventoryId[:-4]

        # Asking MonogoDB if item exists

        item = mycol.find_one({"ngInventoryId": ngInventoryId})
        if not item:
            print(ngInventoryId + ': položka neexistuje v MongoDB')
            continue
        
        if 'localizedFacesAnnotations' in item:
            print(ngInventoryId + ': položka existuje v MongoDB, ale je již rozpoznána')
            continue

        # Creates img path

        imagePath = collectionLocalDirectory + '/' + filename
        print(imagePath)

        # Get image size

        im = Image.open(imagePath)
        imageWidth = im.width
        imageHeight = im.height

        # Saving Results from Google

        result = detect_faces(imagePath, imageWidth, imageHeight)
        print(ngInventoryId + ': položka existuje v MongoDB a dosud nebyla rozpoznána. Zapisuji: ' + str(result))

        # Writing to MonogoDB

        myquery = {"ngInventoryId": ngInventoryId}
        newvalues = {"$set": {"localizedFacesAnnotations": result}}
        mycol.update_one(myquery, newvalues)

        # breaking counter
        if counter == maxTasks:
            break

        counter += 1

# Asking Google for labels

def detect_labels(path):
    """Detects labels in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    responses = []

    for label in labels:
        responses.append({
            "description": label.description,
            "score": label.score,
        })

    return responses

# Checks labels on local images and writes results to MongoDB

def getLabels(counter):
    print('Startuji rozpoznávání štítků pro celý obraz')
    for filename in os.listdir(collectionLocalDirectory):
        # Gets inventory ID

        ngInventoryId = str(filename)
        ngInventoryId = ngInventoryId[:-4]

        # Asking MonogoDB if item exists

        item = mycol.find_one({"ngInventoryId": ngInventoryId})
        if not item:
            print(ngInventoryId + ': položka neexistuje v MongoDB')
            continue

        if 'labelAnnotations' in item:
            print(ngInventoryId + ': položka existuje v MongoDB, ale je již rozpoznána')
            continue

        # Creates img path
        imagePath = collectionLocalDirectory + '/' + filename
        print(imagePath)

        # Saving Results from Google

        result = detect_labels(imagePath)
        print(ngInventoryId + ': položka existuje v MongoDB a dosud nebyla rozpoznána. Zapisuji: ' + str(result))

        # Writing to MonogoDB

        myquery = {"ngInventoryId": ngInventoryId}
        newvalues = {"$set": {"labelAnnotations": result}}
        mycol.update_one(myquery, newvalues)

        # breaking counter
        if counter == maxTasks:
            break

        counter += 1

# Asking Google for Colors

def detect_properties(path):
    """Detects image properties in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.image_properties(image=image)
    props = response.image_properties_annotation

    responses = []

    for color in props.dominant_colors.colors:
        responses.append({
            "fraction": color.pixel_fraction,
            "r": str(color.color.red),
            "g": str(color.color.green),
            "b": str(color.color.blue),
            "a": str(color.color.alpha),
        })

    return responses

# Checks colors on local images and writes results to MongoDB

def getProperties(counter):
    print('Startuji rozpoznávání barev')
    for filename in os.listdir(collectionLocalDirectory):
        # Gets inventory ID

        ngInventoryId = str(filename)
        ngInventoryId = ngInventoryId[:-4]

        # Asking MonogoDB if item exists

        item = mycol.find_one({"ngInventoryId": ngInventoryId})
        if not item:
            print(ngInventoryId + ': položka neexistuje v MongoDB')
            continue

        if 'propertiesAnnotations' in item:
            print(ngInventoryId + ': položka existuje v MongoDB, ale je již rozpoznána')
            continue

        # Creates img path
        imagePath = collectionLocalDirectory + '/' + filename
        print(imagePath)

        # Saving Results from Google

        result = detect_properties(imagePath)
        print(ngInventoryId + ': položka existuje v MongoDB a dosud nebyla rozpoznána. Zapisuji: ' + str(result))

        # Writing to MonogoDB

        myquery = {"ngInventoryId": ngInventoryId}
        newvalues = {"$set": {"propertiesAnnotations": result}}
        mycol.update_one(myquery, newvalues)

        # breaking counter
        if counter == maxTasks:
            break

        counter += 1

# Calls functions

maxTasks = 1000

getProperties(0)
getLabels(0)
getFaces(0)
getObjects(0)





