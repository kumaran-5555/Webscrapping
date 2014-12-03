__author__ = 'serajago'

import os
import sys

import webkitBrowser

# return 'display: none; ' in [e.attribute('style') for e in w.findElement('div[id="load-more-results"]')]


mobilesUrl = 'http://www.flipkart.com/mobiles/pr?sid=tyy,4io&otracker=nmenu_sub_electronics_0_All%20Brands'
sys.exit(0)

brandsDataFile = open("brandsData.tsv", "r", encoding="utf-8")
productLinksScrapeStsFile = open("productLinksScrapeSts.tsv", "r", encoding="utf-8")
productsLinkDataFile = open("productsLinkData.tsv", "a", encoding="utf-8")

productLinksScrapeSts = []
brandsData = []

for l in brandsDataFile:
    brandsData.append(l[:-1])

for l in productLinksScrapeStsFile:
    if l[:-1].split('\t')[1] == "DONE":
        productLinksScrapeSts.append((l[:-1].split('\t')[0]))
productLinksScrapeSts.close()
productLinksScrapeStsFile = open("productLinksScrapeSts.tsv", "w", encoding="utf-8")

for brand in productLinksScrapeSts:
    productLinksScrapeStsFile.write(brand+"\tDONE\n")

productLinksScrapeStsFile.flush()
print(productLinksScrapeSts)
print(brandsData)

b = webkitBrowser.Browser(gui=True, loadImages=False)

for brand in brandsData:
    if brand in productLinksScrapeSts:
        print("sts: Skipping brand "+brand)
        continue
    print("sts: Processing brands " + brand)
    b.loadPage(b.decodedUrl(mobilesUrl))
    b.clickElement('ul[id="brand"]>li[title="' + brand + '"]>a')
    b.waitSecs(5)
    sts = b.scrollPageTill(user_stopScrolling, maxTries=100, timerStep=750)
    print("sts: Initial scroll done")
    if not sts:
        print("sts: Brand failed "+brand)
        productLinksScrapeStsFile.write(brand+"\tFAILED\n")
        productLinksScrapeStsFile.flush()
        continue

    sts = b.clickElementTill('div[id="show-more-results"][style="display: block; "]', user_stopClicking,
                       afterClick=user_afterClick, maxTries=5)
    if not sts:
        print("sts: Brand failed "+brand)
        productLinksScrapeStsFile.write(brand+"\tFAILED\n")
        continue
    print("sts: Final scroll done")
    productsLinkData = []
    productsCount = 0
    # in stock products
    for p in b.findElement('a[class="pu-image fk-product-thumb "]'):
        productsCount += 1
        productsLinkData.append(p.attribute("href"))
        productsLinkDataFile.write(brand + "\t" + p.attribute("href")+"\n")
    # out of stock products
    for p in b.findElement('a[class="pu-image fk-product-thumb oos"]'):
        productsCount += 1
        productsLinkData.append(p.attribute("href"))
        productsLinkDataFile.write(brand + "\t" + p.attribute("href")+"\n")
    print("sts: Total product counts " + str(productsCount))
    productLinksScrapeStsFile.write(brand+"\tDONE\n")
    productLinksScrapeStsFile.flush()
    productsLinkDataFile.flush()





# b.clickElement('ul[id="brand"]>li[title="Samsung"]>a')
# for e in b.findElement('div[class="sdCheckbox fliters-list "]>label>a'):
#    print(e.attribute("href"))
#b.scrollPageTill(user_stopScrolling, maxTries=100)
#print("Scrooled")
#b.clickElementTill('div[id="show-more-results"][style="display: block; "]', user_stopClicking, afterClick=user_afterClick, maxTries=1000)
#print("clicked")
#b.waitSecs(1)
