from requests_html import HTMLSession
import urllib.request
session = HTMLSession()

def pcgScrap(pageUrl, scrapedWebsite):

    ng = session.get(pageUrl)

    # IF FINDS ITEM'S NAME, IT CONTINUES

    checkArtworkPage = ng.html.find('.breadcrumbs', first=True) # Search for breadcrumbs and if there are, it continues

    if not checkArtworkPage == None:

        artworkData = {}

        # SCRAPPING ITEM NAME

        itemName = ng.html.find('h1', first=True)
        if not itemName == None:
            itemName = itemName.text
            titleStart = itemName.find(':')+2 # searches for ':' for finding the start of title
            artworkData['Title'] = ''.join(list(itemName)[titleStart:])  # cut all letters before titleStart
        else:
            artworkData['Title'] = 'n/a'

        # SCRAPPING AUTHOR

        author = ng.html.find('h1', first=True)
        if not author == None:
            author = author.text
            authorEnd = author.find(':')  # searches for ':' for finding the end of author
            artworkData['Author'] = ''.join(list(author)[:authorEnd])  # cut all letters after authorEnd
        else:
            artworkData['Author'] = 'n/a'

        # SCRAPPING CREATION DATE

        creationDate = ng.html.find('#page-content', first=True)
        if not creationDate == None:
            creationDate = creationDate.text
            creationDateStart = creationDate.find('datace:') + 8
            creationDateEnd = creationDate.find('\ntechnika:')
            artworkData['Creation Date'] = ''.join(list(creationDate)[creationDateStart:creationDateEnd])  # cut all letters before creationDateStart and after creationDateEnd
        else:
            artworkData['Creation Date'] = 'n/a'

        # SCRAPPING MATERIAL

        material = ng.html.find('#page-content', first=True)
        if not material == None:
            material = material.text
            materialStart = creationDate.find('materiál') + 10
            if material.find('\ndalší díla umělce') != -1: # if page contains 'dalsi dila umelce' it sets materialEnd by its start
                materialEnd = material.find('\ndalší díla umělce') -2
            else:
                materialEnd = material.find('\n\n$(function ()')
            artworkData['Material'] = ''.join(list(material)[materialStart:materialEnd])  # cut all letters before xStart and after xEnd
        else:
            artworkData['Material'] = 'n/a'

        # SCRAPPING TECHNIQUE

        technique = ng.html.find('#page-content', first=True)
        if not technique == None:
            technique = technique.text
            techniqueStart = technique.find('technika:') + 10
            techniqueEnd = technique.find('\nmateriál:')
            artworkData['Technique'] = ''.join(list(technique)[techniqueStart:techniqueEnd])  # cut all letters before xStart and after xEnd
        else:
            artworkData['Technique'] = 'n/a'


        # SCRAPPING INVENTORY ID

        inventoryId = ng.html.find('#page-content', first=True)
        if not inventoryId == None:
            inventoryId = inventoryId.text
            inventoryIdStart = inventoryId.find('inv. č.:') + 9
            inventoryIdEnd = inventoryId.find('\n\nsbírka:')
            artworkData['Inventory ID'] = ''.join(list(technique)[inventoryIdStart:inventoryIdEnd])  # cut all letters before xStart and after xEnd
            artworkData['Inventory ID'] = artworkData['Inventory ID'].replace(" ", "")
        else:
            artworkData['Inventory ID'] = 'n/a'

            # SCRAPPING SUBCOLLECTION

        subcollection = ng.html.find('#page-content', first=True)
        if not subcollection == None:
            subcollection = subcollection.text
            subcollectionStart = subcollection.find('sbírka:') + 8
            subcollectionEnd = subcollection.find('\ndatace:')
            artworkData['Subcollection'] = ''.join(
                list(technique)[subcollectionStart:subcollectionEnd])  # cut all letters before xStart and after xEnd
        else:
            artworkData['Subcollection'] = 'n/a'

        # ADDING COLLECTION

        artworkData['Collection'] = 'Prague City Gallery'
        collectionShortcut = 'PCG'

        # SAVING URL

        artworkData['Url'] = pageUrl

        # ADDING KEY

        key = collectionShortcut + '-' + artworkData['Inventory ID']
        artworkData['Key'] = key

        # SCRAPPING IMAGE

        def dlJpg(iiUrl, filePath, ngKey):
            imagePath = 'temp/' + filePath + ngKey + '.jpg'
            artworkData['Image ID'] = ngKey + '.jpg'
            urllib.request.urlretrieve(iiUrl, imagePath)

        iiUrl = ng.html.find('.active-zoom-image', first=True)
        if iiUrl != None and 'no-image' not in str(iiUrl):  # if image exists and its name doesn't contain 'no-image'
            iiUrl = iiUrl.attrs
            iiUrl = iiUrl.get("src")  # takes value of src attribute
            iiUrl = scrapedWebsite + iiUrl
            print(iiUrl)
            dlJpg(iiUrl, '/', key)

        # OUTPUT

        print(artworkData)
        return artworkData

    else:
        print('Nothing here')
