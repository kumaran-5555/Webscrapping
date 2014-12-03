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
    if l[:-1].split("\t") == "DONE":
        productsSpecScrapeSts.append(l[:-1].split("\t")[0])

productsSpecScrapeStsFile.close()
productsSpecScrapeStsFile = open("productsSpecScrapeStsFile.tsv", "w", encoding="utf-8")

for product in productsSpecScrapeSts:
    productsSpecScrapeStsFile.write(product + "\tDONE")
productsSpecScrapeStsFile.flush()

print(productsLinkData)
print(productsSpecScrapeSts)

b = webkitBrowser.Browser(gui=True, loadImages=False)

for product in productsLinkData:
    if product in productsSpecScrapeSts:
        print("sts: Skipping product " + product[0:25] + "...")
        continue
    print("sts: Processing product " + product[0:25])
    b.loadPage(b.decodedUrl(baseUrl + product))
    b.waitSecs(5)
    for t in b.findElement('table[class="specTable"]>tbody'):
        tableHeader = t.findAll('tr>th')[0].toInnerXml().strip().lower().replace(" ", "_")
        for td in t.findAll('tr>td'):
            if td.attribute("class")=="specsKey":
                print(tableHeader+td.toInnerXml().strip())
            else:
                print(td.toInnerXml().strip())
    break