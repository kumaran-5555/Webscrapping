__author__ = 'serajago'

import webkitBrowser
import sys

baseUrl = "http://www.flipkart.com"
productsLinkDataFile = open("productsLinkData.tsv", "r", encoding="utf-8")
mobilePicScrapeStsFile = open("mobilePicScrapeStsFile.tsv", "r", encoding="utf-8")
mobilePicDataFile = open("mobilePicDataFile.tsv", "a", encoding="utf-8")

mobilePicScrapeSts = []
productsLinkData = []

for l in productsLinkDataFile:
    productsLinkData.append(l[:-1].split("\t")[1])

for l in mobilePicScrapeStsFile:
    if l[:-1].split("\t")[1] == "DONE":
        mobilePicScrapeSts.append(l[:-1].split("\t")[0])

mobilePicScrapeStsFile.close()
mobilePicScrapeStsFile = open("mobilePicScrapeStsFile.tsv", "w", encoding="utf-8")

for product in mobilePicScrapeSts:
    mobilePicScrapeStsFile.write(product + "\tDONE\n")
mobilePicScrapeStsFile.flush()

print(productsLinkData)
print(mobilePicScrapeSts)

b = webkitBrowser.Browser(gui=True, loadImages=False, javaScriptEnabled=False)
productCount = 0
for product in productsLinkData:
    productCount += 1
    if product in mobilePicScrapeSts:
        print("sts: Skipping product " + product[0:25] + "...")
        continue
    print("sts: Processing product " + product[0:25])
    # clear the content for reset and error anding
    b.setHtml('<html><head></head><body>No content loaded</body></html>')
    b.loadPage(b.decodedUrl(baseUrl + product))

    picsUrls = ""
    for e in b.findElement('div[class="imgWrapper"]>img'):
        if e.attribute('data-zoomimage') == "":
            picsUrls = picsUrls + "|" + e.attribute('data-src')
        else:
            picsUrls = picsUrls + "|" + e.attribute('data-zoomimage')

    if picsUrls != "":
        mobilePicDataFile.write(product + "\t" + picsUrls + "\n")
        mobilePicScrapeStsFile.write(product + "\tDONE\n")
    else:
        mobilePicScrapeStsFile.write(product + "\tFAILED\n")

    mobilePicScrapeStsFile.flush()
    mobilePicDataFile.flush()
    print("sts: done product " + product + " total " + str(productCount))

mobilePicDataFile.close()
mobilePicScrapeStsFile.close()

