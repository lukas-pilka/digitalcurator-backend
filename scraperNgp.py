from requests_html import HTMLSession
import urllib.request
session = HTMLSession()

def oneScrap(pageUrl, scrapedWebsite):

    ng = session.get(pageUrl)

    # IF FINDS ITEM'S NAME, IT CONTINUES

    ngItemName = ng.html.find('.nadpis-dielo', first=True)

    if not ngItemName == None:

        artworkData = {}

        # SCRAPPING ITEM NAME

        ngItemName = ng.html.find('.nadpis-dielo', first=True)
        if not ngItemName == None:
            artworkData['Title'] = ngItemName.text
        else:
            artworkData['Title'] = 'n/a'

        # SCRAPPING AUTHOR

        ngAuthor = ng.html.find('.inline', first=True)
        if not ngAuthor == None:
            artworkData['Author'] = ngAuthor.text
        else:
            artworkData['Author'] = 'n/a'

        # SCRAPPING CREATION DATE

        ngCreationDate = ng.html.find('tr', containing='datace:', first=True)
        if not ngCreationDate == None:
            artworkData['Creation Date'] = ''.join(list(ngCreationDate.text)[8:]) # CUT X LETTERS FROM BEGINNING
        else:
            artworkData['Creation Date'] = 'n/a'

        # SCRAPPING DIMENSIONS

        ngDimensions = ng.html.find('tr', containing='rozměry:', first=True)
        if not ngDimensions == None:
            artworkData['Dimensions'] = ''.join(list(ngDimensions.text)[9:]) # CUT X LETTERS FROM BEGINNING
        else:
            artworkData['Dimensions'] = 'n/a'

        # SCRAPPING CURATED SETS

        ngCuratedSets = ng.html.find('tr', containing='tematické celky:', first=True)
        if not ngCuratedSets == None:
            artworkData['Curated Sets'] = ''.join(list(ngCuratedSets.text)[17:]) # CUT X LETTERS FROM BEGINNING
        else:
            artworkData['Curated Sets'] = 'n/a'

        # SCRAPPING MATERIAL

        ngMaterial = ng.html.find('tr', containing='materiál:', first=True)
        if not ngMaterial == None:
            artworkData['Material'] = ''.join(list(ngMaterial.text)[10:]) # CUT X LETTERS FROM BEGINNING
        else:
            artworkData['Material'] = 'n/a'

        # SCRAPPING TECHNIQUE

        ngTechnique = ng.html.find('tr', containing='technika:', first=True)
        if not ngTechnique == None:
            artworkData['Technique'] = ''.join(list(ngTechnique.text)[10:]) # CUT X LETTERS FROM BEGINNING
        else:
            artworkData['Technique'] = 'n/a'

        # SCRAPPING SIGNATURE

        ngSignature = ng.html.find('tr', containing='značení:', first=True)
        if not ngSignature == None:
            artworkData['Artist signature'] = ''.join(list(ngSignature.text)[9:]) # CUT X LETTERS FROM BEGINNING
        else:
            artworkData['Artist signature'] = 'n/a'

        # SCRAPPING INVENTORY ID

        ngInventoryId = ng.html.find('tr', containing='inventární číslo:', first=True)
        if not ngInventoryId == None:
            ngInventoryId = ''.join(list(ngInventoryId.text)[18:]) # CUT X LETTERS FROM BEGINNING
            ngInventoryId = ngInventoryId.replace(" ", "-")
            artworkData['Inventory ID'] = ngInventoryId
        else:
            artworkData['Inventory ID'] = 'n/a'

        # SCRAPPING SUBCOLLECTION

        ngSubcollection = ng.html.find('tr', containing='sbírka:', first=True)
        if not ngSubcollection == None:
            artworkData['Subcollection'] = ''.join(list(ngSubcollection.text)[8:]) # CUT X LETTERS FROM BEGINNING
        else:
            artworkData['Subcollection'] = 'n/a'

        # SCRAPPING LICENCE

        ngLicence = ng.html.find('tr', containing='licence:', first=True)
        if not ngLicence == None:
            artworkData['Licence'] = ''.join(list(ngLicence.text)[9:]) # CUT X LETTERS FROM BEGINNING
        else:
            artworkData['Licence'] = 'n/a'

        # SCRAPPING DESCRIPTION

        ngDescription = ng.html.find('.description', first=True)
        if not ngDescription == None:
            artworkData['Description'] = ngDescription.text
        else:
            artworkData['Description'] = 'n/a'

        # ADDING COLLECTION

        artworkData['Collection'] = 'National Gallery in Prague'
        collectionShortcut = 'NGP'

        # SAVING URL

        artworkData['Url'] = pageUrl

        # ADDING KEY

        ngKey = collectionShortcut + '-' + ngInventoryId
        artworkData['Key'] = ngKey

        # SCRAPPING IMAGE

        def dlJpg(iiUrl, filePath, ngKey):
            imagePath = 'temp/' + filePath + ngKey + '.jpg'
            artworkData['Image ID'] = ngKey + '.jpg'
            urllib.request.urlretrieve(iiUrl, imagePath)

        iiUrl = ng.html.find('.img-dielo', first=True)
        if not iiUrl == None:
            iiUrl = iiUrl.attrs
            iiUrl = iiUrl.get("src")  # TAKES VALUE OF SRC ATTRIBUTE
            iiUrl = scrapedWebsite + iiUrl
            dlJpg(iiUrl, '/', ngKey)

        else:
            iiUrl = 'n/a'

        # OUTPUT

        print(artworkData)
        return artworkData

    else:
        print('Nothing here')


