__author__ = 'serajago'

import webkitBrowser
import sys

baseUrl = "http://www.flipkart.com"
productsLinkDataFile = open("productsLinkData.tsv", "r", encoding="utf-8")
productsSpecScrapeStsFile = open("productsSpecScrapeStsFile.tsv", "r", encoding="utf-8")
productsSpecDataFile = open("productsSpecDataFile.tsv", "a", encoding="utf-8")

productsSpecScrapeSts = []
productsLinkData = []

for l in productsLinkDataFile:
    productsLinkData.append(l[:-1].split("\t")[1])

for l in productsSpecScrapeStsFile:
    if l[:-1].split("\t")[1] == "DONE":
        productsSpecScrapeSts.append(l[:-1].split("\t")[0])

productsSpecScrapeStsFile.close()
productsSpecScrapeStsFile = open("productsSpecScrapeStsFile.tsv", "w", encoding="utf-8")

for product in productsSpecScrapeSts:
    productsSpecScrapeStsFile.write(product + "\tDONE\n")
productsSpecScrapeStsFile.flush()

print(productsLinkData)
print(productsSpecScrapeSts)

b = webkitBrowser.Browser(gui=True, loadImages=False, javaScriptEnabled=False)
productCount = 0
for product in productsLinkData:
    productCount += 1
    if product in productsSpecScrapeSts:
        print("sts: Skipping product " + product[0:25] + "...")
        continue
    print("sts: Processing product " + product[0:25])
    # clear the content for reset and error anding
    b.setHtml('<html><head></head><body>No content loaded</body></html>')
    b.loadPage(b.decodedUrl(baseUrl + product))
    outputStr = ""

    if len(b.findElement('span[class="selling-price omniture-field"]')) > 0:
        outputStr = outputStr + "OfficePrice|" + b.findElement('span[class="selling-price omniture-field"]')[
            0].toInnerXml()
    else:
        outputStr = outputStr + "OfficePrice|"

    if len(b.findElement('div[class="prices"]>span[class="price"]')) > 0:
        outputStr = outputStr + "\t" + "mrpPrice|" + b.findElement('div[class="prices"]>span[class="price"]')[
            0].toInnerXml()
    else:
        outputStr = outputStr + "\t" + "mrpPrice|"

    if len(b.findElement(
        'div[class="title-wrap line fk-font-family-museo section omniture-field"]>h1[class="title"]')) >0:
        outputStr = outputStr + "\t" + "name|" + b.findElement(
            'div[class="title-wrap line fk-font-family-museo section omniture-field"]>h1[class="title"]')[ \
            0].toInnerXml()
    else:
        outputStr = outputStr + "\t" + "name|"

    if len(b.findElement(
            'div[class="title-wrap line fk-font-family-museo section omniture-field"]>span[class="subtitle"]')) > 0:
        outputStr = outputStr + "\t" + "color|" + b.findElement(
            'div[class="title-wrap line fk-font-family-museo section omniture-field"]>span[class="subtitle"]')[ \
            0].toInnerXml()
    else:
        outputStr = outputStr + "\t" + "color|"

    specStr = ""
    # spec scrapping
    for t in b.findElement('table[class="specTable"]>tbody'):
        specHeader = t.findAll('tr>th')[0].toInnerXml().strip().lower()
        for td in t.findAll('tr>td'):
            if td.attribute("class") == "specsKey":
                specKey = td.toInnerXml().strip()
            else:
                specVal = td.toInnerXml().strip().replace("\n","")
                specStr = specStr + specHeader + "|" + specKey + "|" + specVal + "|"
    if specStr != "":
        productsSpecDataFile.write(product + "\t" + outputStr +"\t" + "spec|" + specStr + "\n")
        productsSpecScrapeStsFile.write(product + "\tDONE\n")
    else:
        productsSpecScrapeStsFile.write(product + "\tFAILED\n")

    productsSpecScrapeStsFile.flush()
    productsSpecDataFile.flush()
    print("sts: done product " + product + " total " + str(productCount))
productsSpecDataFile.close()
productsSpecScrapeStsFile.close()
