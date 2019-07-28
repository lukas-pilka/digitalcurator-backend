
import pymongo
import csv

# Connecting MongoDB

client = pymongo.MongoClient("mongodb+srv://lukaspilka:Apollo11@digitalcurator-hw3um.mongodb.net/test?retryWrites=true&w=majority")
mydb = client["artpieces"]
mycol = mydb["items"]

# Selecting CSV for import

csvForImport = 'collections/sbirka-grafiky-items.csv'

# Counter for writing process

counter = 0

# Loading CSV

with open(csvForImport) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        mydict = {"ngItemName": row[0], "ngAuthor": row[1], "ngCreationDate": row[2], "ngSizes": row[3], "ngTopicUnits": row[4], "ngMaterial": row[5], "ngMarking": row[6], "ngInventoryId": row[7], "ngCollection": row[8], "ngLicence": row[9], "ngDescription": row[10]}
        print(mydict)
        x = mycol.insert_one(mydict)
        line_count += 1
        print(f'Processed {line_count} lines.')

        # breaking counter
        if counter == 500:
            break

        counter += 1





