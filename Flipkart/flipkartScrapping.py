__author__ = 'serajago'

import webkitBrowser
import sys
import os

def user_stopScrolling(w):
	return 'display: block; ' in [e.attribute('style') for e in w.findElement('div[id="show-more-results"]')] or 'display: block; ' in [e.attribute('style') for e in w.findElement('div[id="no-more-results"]')]

def user_stopClicking(w):
	return 'display: block; ' in [e.attribute('style') for e in w.findElement('div[id="no-more-results"]')]

def user_afterClick(w):
	print ("user after click process ")
	w.scrollPageTill(user_stopScrolling, maxTries=500)
	#return 'display: none; ' in [e.attribute('style') for e in w.findElement('div[id="load-more-results"]')]



b = webkitBrowser.Browser(gui=True, loadImages=False)
#b.loadPage(b.decodedUrl('http://www.flipkart.com/mobiles/pr?p[]=facets.brand%255B%255D%3DSamsung&sid=tyy%2C4io&ref=1549eee4-5e08-4d7f-bda2-2868950c091f'))
b.loadPage(b.decodedUrl('http://www.flipkart.com/mobiles/pr?sid=tyy,4io&otracker=nmenu_sub_electronics_0_All%20Brands'))

brandsList = open("brandsList.tsv","w",encoding="utf-8")

for e in b.findElement('ul[id="brand"]>li'):
    brandsList.write()

#b.clickElement('ul[id="brand"]>li[title="Samsung"]>a')
#for e in b.findElement('div[class="sdCheckbox fliters-list "]>label>a'):
#    print(e.attribute("href"))
b.scrollPageTill(user_stopScrolling, maxTries=100)
print("Scrooled")
b.clickElementTill('div[id="show-more-results"][style="display: block; "]', user_stopClicking, afterClick=user_afterClick, maxTries=1000)
print("clicked")
b.waitSecs(1)