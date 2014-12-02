'''
__author__ = 'serajago'
import webkitBrowser
import pickle

allBrandsUrlFile = open("allBrandsUrl.pkl","wb")

b = webkitBrowser.Browser(gui=False, loadImages=False)
b.loadPage(b.decodedUrl("http://www.gsmarena.com/makers.php3"))
allBrandsUrl = []

for brandsRow in b.findElement('div[class="st-text"]>table>tbody>tr'):
    for brands in brandsRow.findAll('td>a[href]'):
        if baseUrl+"/"+brands.attribute("href") not in allBrandsUrl:
            allBrandsUrl.append(baseUrl+"/"+brands.attribute("href"))

print(allBrandsUrl)

pickle.dump(allBrandsUrl, allBrandsUrlFile)
allBrandsUrlFile.close()

import pickle
import  webkitBrowser
brandsToPages = {}
brandsToPagesFile = open("brandsToPages.pkl", "wb")
baseUrl = "http://www.gsmarena.com"
brands = pickle.load(open("allBrandsUrl.pkl","rb"))
browser = webkitBrowser.Browser(gui=False, loadImages=False)
for b in brands:
    browser.loadPage(browser.decodedUrl(b))
    pages = browser.findElement('div[class="nav-pages"]>a')
    brandsToPages[b] = []
    for p in pages:
        brandsToPages[b].append(baseUrl+"/"+p.attribute("href"))
    print(brandsToPages[b])

pickle.dump(brandsToPages, brandsToPagesFile)
brandsToPagesFile.close()

'''


import pickle

