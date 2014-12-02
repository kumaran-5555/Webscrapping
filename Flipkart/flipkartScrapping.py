__author__ = 'serajago'

import webkitBrowser
import sys
import os


def user_stopScrolling(w):
    return 'display: block; ' in [e.attribute('style') for e in
                                  w.findElement('div[id="show-more-results"]')] or 'display: block; ' in [
        e.attribute('style') for e in w.findElement('div[id="no-more-results"]')]


def user_stopClicking(w):
    return 'display: block; ' in [e.attribute('style') for e in w.findElement('div[id="no-more-results"]')] or 'display: block; ' in [
        e.attribute('style') for e in w.findElement('div[id="no-more-results"]')]


def user_afterClick(w):
    print("user after click process ")
    w.scrollPageTill(user_stopScrolling, maxTries=100)

# return 'display: none; ' in [e.attribute('style') for e in w.findElement('div[id="load-more-results"]')]


mobilesUrl = 'http://www.flipkart.com/mobiles/pr?sid=tyy,4io&otracker=nmenu_sub_electronics_0_All%20Brands'
brandsListFile = open("brandsList.tsv", "w", encoding="utf-8")
brandsListProductsDoneFile = open("brandsListProductsDone.tsv", "r", encoding="utf-8")
productsLinkFile = open("productsLink.tsv", "a", encoding="utf-8")

brandsListProductsDone = []
brandsList = []

b = webkitBrowser.Browser(gui=True, loadImages=False)

# b.loadPage(b.decodedUrl('http://www.flipkart.com/mobiles/pr?p[]=facets.brand%255B%255D%3DSamsung&sid=tyy%2C4io&ref=1549eee4-5e08-4d7f-bda2-2868950c091f'))
b.loadPage(b.decodedUrl(mobilesUrl))

for e in b.findElement('ul[id="brand"]>li'):
    brandsListFile.write(e.attribute("title") + "\n")
    brandsList.append(e.attribute("title"))
brandsListFile.close()

for l in brandsListProductsDoneFile:
    if l[:-1].split('\t')[1] == "DONE":
        brandsListProductsDone.append((l[:-1].split('\t')[0]))
brandsListProductsDoneFile.close()
brandsListProductsDoneFile = open("brandsListProductsDone.tsv", "w", encoding="utf-8")

for brand in brandsListProductsDone:
    brandsListProductsDoneFile.write(brand+"\tDONE\n")

brandsListProductsDoneFile.flush()
print(brandsListProductsDone)
print(brandsList)


for brand in brandsList:
    if brand in brandsListProductsDone:
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
        brandsListProductsDoneFile.write(brand+"\tFAILED\n")
        brandsListProductsDoneFile.flush()
        continue

    sts = b.clickElementTill('div[id="show-more-results"][style="display: block; "]', user_stopClicking,
                       afterClick=user_afterClick, maxTries=5)
    if not sts:
        print("sts: Brand failed "+brand)
        brandsListProductsDoneFile.write(brand+"\tFAILED\n")
        continue
    print("sts: Final scroll done")
    productsLink = []
    productsCount = 0
    # in stock products
    for p in b.findElement('a[class="pu-image fk-product-thumb "]'):
        productsCount += 1
        productsLink.append(p.attribute("href"))
        productsLinkFile.write(brand + "\t" + p.attribute("href")+"\n")
    # out of stock products
    for p in b.findElement('a[class="pu-image fk-product-thumb oos"]'):
        productsCount += 1
        productsLink.append(p.attribute("href"))
        productsLinkFile.write(brand + "\t" + p.attribute("href")+"\n")
    print("sts: Total product counts " + str(productsCount))
    brandsListProductsDoneFile.write(brand+"\tDONE\n")
    brandsListProductsDoneFile.flush()
    productsLinkFile.flush()





# b.clickElement('ul[id="brand"]>li[title="Samsung"]>a')
# for e in b.findElement('div[class="sdCheckbox fliters-list "]>label>a'):
#    print(e.attribute("href"))
#b.scrollPageTill(user_stopScrolling, maxTries=100)
#print("Scrooled")
#b.clickElementTill('div[id="show-more-results"][style="display: block; "]', user_stopClicking, afterClick=user_afterClick, maxTries=1000)
#print("clicked")
#b.waitSecs(1)
