from requests_html import HTMLSession
import urllib.request
session = HTMLSession()

def mgbScrap(pageUrl, scrapedWebsite):

    ng = session.get(pageUrl)

    # IF FINDS ITEM'S NAME, IT CONTINUES

    ItemName = ng.html.find('.nadpis-dielo', first=True)

    if not ItemName == None:

        artworkData = {}

        # SCRAPPING ITEM NAME

        ItemName = ng.html.find('.nadpis-dielo', first=True)
        if not ItemName == None:
            artworkData['Title'] = ItemName.text
        else:
            artworkData['Title'] = 'n/a'

        # SCRAPPING AUTHOR

        Author = ng.html.find('.inline', first=True)
        if not Author == None:
            artworkData['Author'] = Author.text
        else:
            artworkData['Author'] = 'n/a'

        # SCRAPPING CREATION DATE

        CreationDate = ng.html.find('tr', containing='datace:', first=True)
        if not CreationDate == None:
            artworkData['Creation Date'] = ''.join(list(CreationDate.text)[8:]) # CUT X LETTERS FROM BEGINNING
        else:
            artworkData['Creation Date'] = 'n/a'

        # SCRAPPING CREATION PLACE

        CreationPlace = ng.html.find('tr', containing='místo vzniku:', first=True)
        if not CreationPlace == None:
            artworkData['Creation Place'] = ''.join(list(CreationPlace.text)[13:])  # CUT X LETTERS FROM BEGINNING
        else:
            artworkData['Creation Place'] = 'n/a'

        # SCRAPPING ACQUISITION DATE

        AcquisitionDate = ng.html.find('tr', containing='datum akvizice:', first=True)
        if not AcquisitionDate == None:
            artworkData['Acquisition Date'] = ''.join(list(AcquisitionDate.text)[15:])  # CUT X LETTERS FROM BEGINNING
        else:
            artworkData['Acquisition Date'] = 'n/a'

        # SCRAPPING DIMENSIONS

        Dimensions = ng.html.find('tr', containing='rozměry:', first=True)
        if not Dimensions == None:
            artworkData['Dimensions'] = ''.join(list(Dimensions.text)[9:]) # CUT X LETTERS FROM BEGINNING
        else:
            artworkData['Dimensions'] = 'n/a'

        # SCRAPPING CURATED SETS

        CuratedSets = ng.html.find('tr', containing='tematické celky:', first=True)
        if not CuratedSets == None:
            artworkData['Curated Sets'] = ''.join(list(CuratedSets.text)[17:]) # CUT X LETTERS FROM BEGINNING
        else:
            artworkData['Curated Sets'] = 'n/a'

        # SCRAPPING MATERIAL

        Material = ng.html.find('tr', containing='materiál:', first=True)
        if not Material == None:
            artworkData['Material'] = ''.join(list(Material.text)[10:]) # CUT X LETTERS FROM BEGINNING
        else:
            artworkData['Material'] = 'n/a'

        # SCRAPPING TECHNIQUE

        Technique = ng.html.find('tr', containing='technika:', first=True)
        if not Technique == None:
            artworkData['Technique'] = ''.join(list(Technique.text)[10:]) # CUT X LETTERS FROM BEGINNING
        else:
            artworkData['Technique'] = 'n/a'

        # SCRAPPING SIGNATURE

        Signature = ng.html.find('tr', containing='značení:', first=True)
        if not Signature == None:
            artworkData['Artist signature'] = ''.join(list(Signature.text)[9:]) # CUT X LETTERS FROM BEGINNING
        else:
            artworkData['Artist signature'] = 'n/a'

        # SCRAPPING INVENTORY ID

        InventoryId = ng.html.find('tr', containing='inventární číslo:', first=True)
        if not InventoryId == None:
            InventoryId = ''.join(list(InventoryId.text)[18:]) # CUT X LETTERS FROM BEGINNING
            InventoryId = InventoryId.replace(" ", "-")
            artworkData['Inventory ID'] = InventoryId
        else:
            artworkData['Inventory ID'] = 'n/a'

        # SCRAPPING SUBCOLLECTION

        Subcollection = ng.html.find('tr', containing='sbírka:', first=True)
        if not Subcollection == None:
            artworkData['Subcollection'] = ''.join(list(Subcollection.text)[8:]) # CUT X LETTERS FROM BEGINNING
        else:
            artworkData['Subcollection'] = 'n/a'

        # SCRAPPING LICENCE

        Licence = ng.html.find('tr', containing='licence:', first=True)
        if not Licence == None:
            artworkData['Licence'] = ''.join(list(Licence.text)[9:]) # CUT X LETTERS FROM BEGINNING
        else:
            artworkData['Licence'] = 'n/a'

        # SCRAPPING DESCRIPTION

        Description = ng.html.find('.description', first=True)
        if not Description == None:
            artworkData['Description'] = Description.text
        else:
            artworkData['Description'] = 'n/a'

        # ADDING COLLECTION

        artworkData['Collection'] = 'Moravian Gallery in Brno'
        collectionShortcut = 'MGB'

        # SAVING URL

        artworkData['Url'] = pageUrl

        # ADDING KEY

        Key = collectionShortcut + '-' + InventoryId
        artworkData['Key'] = Key

        # SCRAPPING IMAGE

        def dlJpg(iiUrl, filePath, ngKey):
            imagePath = 'temp/' + filePath + ngKey + '.jpg'
            artworkData['Image ID'] = ngKey + '.jpg'
            urllib.request.urlretrieve(iiUrl, imagePath)

        iiUrl = ng.html.find('.img-dielo', first=True)
        if iiUrl != None and 'no-image' not in str(iiUrl):  # if image exists and its name doesn't contain 'no-image'
            iiUrl = iiUrl.attrs
            iiUrl = iiUrl.get("src")  # takes value of src attribute
            iiUrl = scrapedWebsite + iiUrl
            dlJpg(iiUrl, '/', Key)

        # OUTPUT

        print(artworkData)
        return artworkData

    else:
        print('Nothing here')