__author__ = 'serajago'

import webkitBrowser

mobilesUrl = 'http://www.flipkart.com/mobiles/pr?sid=tyy,4io&otracker=nmenu_sub_electronics_0_All%20Brands'
brandsDataFile = open("brandsData.tsv", "w", encoding="utf-8")
brandsData = []

b = webkitBrowser.Browser(gui=True, loadImages=False)

b.loadPage(b.decodedUrl(mobilesUrl))

for e in b.findElement('ul[id="brand"]>li'):
    brandsDataFile.write(e.attribute("title") + "\n")
    brandsData.append(e.attribute("title"))
brandsDataFile.close()



