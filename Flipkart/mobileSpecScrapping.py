__author__ = 'serajago'

import webkitBrowser

productsLinkDataFile = open("productsLinkData.tsv", "r", encoding="utf-8")
productsSpecScrapeStsFile = open("productsSpecScrapeStsFile.tsv", "r", encoding="utf-8")
productsSpecDataFile = open("productsSpecDataFile.tsv", "a", encoding="utf-8")

productsSpecScrapeSts = []
productsLinkData = []

for l in productsLinkDataFile:
    productsLinkData.append(l.split("\t")[1])

for l in productsSpecScrapeStsFile:
    if l[:-1].split("\t") == "DONE":
        productsSpecScrapeSts.append(l[:-1].split("\t")[0])
productsSpecScrapeStsFile.close()
productsSpecScrapeStsFile = open("productsSpecScrapeStsFile.tsv", "w", encoding="utf-8")

for product in productsSpecScrapeSts:
    productsSpecScrapeStsFile.write(product + "\tDONE")
productsSpecScrapeStsFile.flush()

b = webkitBrowser.Browser(gui=True, loadImages=False)

for product in productsLinkData:
    if product in productsLinkData:
        print("sts: Skipping product " + product[0:25] + "...")
        continue
    print("sts: Processing product "+ product[0:25])
    b.loadPage(b.decodedUrl(product))
