from requests_html import HTMLSession
import urllib.request
session = HTMLSession()


def bmvScrap(pageUrl, scrapedWebsite):

        scraping = session.get(pageUrl)

        # IF FINDS ITEM NAME, IT CONTINUES

        checkArtworkPage = scraping.html.find('.detail-item-details', first=True)  # Search for element with class and if there is, it continues

        if not checkArtworkPage == None:

            artworkData = {}

            # SCRAPPING ITEM NAME

            itemName = scraping.html.find('h1', first=True)
            if not itemName == None:
                artworkData['Title'] = itemName.text
            else:
                artworkData['Title'] = 'n/a'

            # SCRAPPING AUTHOR

            author = scraping.html.find('.peopleField .detailFieldValue a', first=True)
            if not author == None:
                artworkData['Author'] = author.text
            else:
                artworkData['Author'] = 'n/a'

            # SCRAPPING CREATION DATE

            creationDate = scraping.html.find('.displayDateField .detailFieldValue', first=True)
            if not creationDate == None:
                artworkData['Creation Date'] = creationDate.text
            else:
                artworkData['Creation Date'] = 'n/a'

            # ACQUISITION DATE

            acquisitionDate = scraping.html.find('.paperSupportField .detailFieldValue', first=True)
            if not acquisitionDate == None:
                artworkData['Acquisition Date'] = acquisitionDate.text
            else:
                artworkData['Acquisition Date'] = 'n/a'

            # SCRAPPING TECHNIQUE

            subcollection = scraping.html.find('.nameField .detailFieldValue a', first=True)
            if not subcollection == None:
                artworkData['Subcollection'] = subcollection.text
            else:
                artworkData['Subcollection'] = 'n/a'

            technique = scraping.html.find('.nameField .detailFieldValue a', first=True)
            if not technique == None:
                artworkData['Technique'] = technique.text
            else:
                artworkData['Technique'] = 'n/a'

            # SCRAPPING MATERIAL

            material = scraping.html.find('.mediumField .detailFieldValue', first=True)
            if not material == None:
                artworkData['Material'] = material.text
            else:
                artworkData['Material'] = 'n/a'

            # SCRAPPING STYLE

            style = scraping.html.find('.periodField .detailFieldValue', first=True)
            if not style == None:
                artworkData['Style'] = style.text
            else:
                artworkData['Style'] = 'n/a'

            # SCRAPPING SIGNATURE

            signature = scraping.html.find('.signedField .detailFieldValue', first=True)
            if not signature == None:
                artworkData['Artist signature'] = signature.text
            else:
                artworkData['Artist signature'] = 'n/a'

            # SCRAPPING DIMENSIONS

            dimensions = scraping.html.find('.dimensionsField .detailFieldValue', first=True)
            if not dimensions == None:
                artworkData['Dimensions'] = dimensions.text
            else:
                artworkData['Dimensions'] = 'n/a'

            # SCRAPPING INVENTORY ID

            inventoryId = scraping.html.find('.invnoField .detailFieldValue', first=True)
            if not inventoryId == None:
                artworkData['Inventory ID'] = inventoryId.text
                artworkData['Inventory ID'] = artworkData['Inventory ID'].replace("/", "-")
            else:
                artworkData['Inventory ID'] = 'n/a'

            # ADDING COLLECTION

            artworkData['Collection'] = 'Belvedere Museum Vienna'
            collectionShortcut = 'BMV'

            # SAVING URL

            artworkData['Url'] = pageUrl

            # ADDING LICENCE

            artworkData['Licence'] = 'iiif'

            # ADDING KEY

            key = collectionShortcut + '-' + artworkData['Inventory ID']
            artworkData['Key'] = key

            # SCRAPPING IMAGE

            def dlJpg(iiUrl, filePath, ngKey):
                imagePath = 'temp' + filePath + ngKey + '.jpg'
                artworkData['Image ID'] = ngKey + '.jpg'
                urllib.request.urlretrieve(iiUrl, imagePath)

            iiUrl = scraping.html.find('.width-img-wrap img', first=True)
            if iiUrl != None and 'no-image' not in str(
                    iiUrl):  # if image exists and its name doesn't contain 'no-image'
                iiUrl = iiUrl.attrs
                iiUrl = iiUrl.get("src")  # takes value of src attribute
                iiUrlCut = iiUrl.find('/preview') # finds place where to cut url
                iiUrl = ''.join(list(iiUrl)[:iiUrlCut]) + '/full' # cuts url and adds ending
                iiUrl = scrapedWebsite + iiUrl
                print(iiUrl)
                dlJpg(iiUrl, '/', key)

            # OUTPUT

            print(artworkData)
            return artworkData

        else:
            print('Nothing here')
