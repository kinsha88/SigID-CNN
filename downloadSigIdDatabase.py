#! Download every sigid image and put it in a class folder for CNN training data
# Images taken from website https://www.sigidwiki.com/wiki/Database
#
# Daniela Bozanic 27/02/22

from bs4 import BeautifulSoup
import requests, os, bs4

url = 'https://www.sigidwiki.com/wiki/Database'
os.makedirs('sigidScrape', exist_ok=True)


# Download the page.
print('Downloading page %s...' % url)
res = requests.get(url)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, 'lxml')


# Find the URL's for each image.
contentTable = soup.find_all('table', {'class': 'wikitable'})[1] # get the second wikitable
if contentTable == []:
    print('Could not find a second wikitable.')
else:
    rows = contentTable.find_all('tr')
    for row in rows[1:]:
        if row.select('td')[0].get('bgcolor') == '#FFDADA': 
            continue # skip rows for discontinued signals
        else:
            #try:
                # Get row name
                # waterfallName = row.select('td')[0].get_text()
                # print('Got row name %s...' % (waterfallName))
                # # Download image
                # waterfallUrl = 'https://www.sigidwiki.com' + row.select('img')[0].get('src')
                # print('Downloading image %s...' % (waterfallUrl))
                # res = requests.get(waterfallUrl)
                # res.raise_for_status()
            # except requests.exceptions.MissingSchema:
            #     # skip this image
            #     print('Skipping an image...')
            #     continue #check
            
            # Go into signal article and scrape more images
            try:
                # Get row name
                waterfallName = row.select('td')[0].get_text()
                print('Got row name %s...' % (waterfallName))

                # Go into signal's article
                articleUrl = 'https://www.sigidwiki.com' + row.select('a')[0].get('href')
                res = requests.get(articleUrl)
                res.raise_for_status()

                # Scrape all image elements
                soup = bs4.BeautifulSoup(res.text, 'lxml')
                imageList = soup.select('a[class="image"]')

                # Go through list of image elements
                for i in range(len(imageList)):
                    try:
                        imageFileURL = 'https://sigidwiki.com' + imageList[i].get('href')
                        res2 = requests.get(imageFileURL)
                        soup2 = bs4.BeautifulSoup(res2.text, 'lxml')
                        imageURL = 'https://sigidwiki.com' + soup2.select('img')[0].get('src') #first item in list is image?
                        print('Downloading image %s...' % (imageURL))
                        res3 = requests.get(imageURL)
                        res3.raise_for_status()

                        # Remove '150px-' at start of some file names
                        fileName = os.path.basename(imageURL)
                        if fileName[0:6] == '150px-':
                            fileName = fileName[6:]
                        
                        # Save and close file
                        imgpath = 'sigidScrape' + r'/' + waterfallName
                        os.makedirs(imgpath, exist_ok=True)
                        print('Saving image...')
                        imageFile = open(os.path.join(imgpath, fileName), 'wb')
                        for chunk in res3.iter_content(100000):
                            imageFile.write(chunk)
                        imageFile.close()

                    except requests.exceptions.MissingSchema:
                        # skip this image
                        print('Core image not found from File site.')
                        continue

            except requests.exceptions.MissingSchema:
                # skip this image
                print('No images found in the article')
                continue




print('Done.')