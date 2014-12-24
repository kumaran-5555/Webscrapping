__author__ = 'serajago'

__author__ = 'serajago'
import json
import scrapperJob
import FlipkartNew.helperFunctions


class MobileSpecJob(scrapperJob.ScrapperJob):
    def __init__(self):
        super().__init__()
        super().initScrapperJob("mobiles_products_seed", "mobiles_specs_seed", __name__, gui=True,
                                javaScriptEnabled=False, database="project005_scrapping_20141216",
                                emptyOutputTable=False)

    def collectData(self, seed):
        '''

        :param seed:
        :return: [productSpecDict, [listOfProductImageLinks]]
        '''
        productSpec = {}
        listOfPicUrls = []
        baseUrl = "http://www.flipkart.com"

        self.browser.setHtml('<html><head></head><body>No content loaded</body></html>')
        self.browser.loadPage(self.browser.decodedUrl(baseUrl + seed))

        if len(self.browser.findElement('div[class="ratings"]>div[class="count"]>span[itemprop="ratingCount"]')) > 0:
            productSpec["ratingCount"] = \
            self.browser.findElement('div[class="ratings"]>div[class="count"]>span[itemprop="ratingCount"]')[
                0].toInnerXml()

        if len(self.browser.findElement('div[class="ratings"]>meta')) > 0:
            productSpec["ratingValue"] = self.browser.findElement('div[class="ratings"]>meta')[0].attribute('content')

        if len(self.browser.findElement('div[class="reviews"]>a>span[itemprop="reviewCount"]')) > 0:
            productSpec["reviewCount"] = self.browser.findElement('div[class="reviews"]>a>span[itemprop="reviewCount"]')[0].toInnerXml()

        if len(self.browser.findElement('span[class="selling-price omniture-field"]')) > 0:
            productSpec["OfferPrice"] = self.browser.findElement('span[class="selling-price omniture-field"]')[
                0].toInnerXml()
        else:
            productSpec["OfferPrice"] = ""

        if len(self.browser.findElement('div[class="prices"]>span[class="price"]')) > 0:
            productSpec["mrpPrice"] = self.browser.findElement('div[class="prices"]>span[class="price"]')[
                0].toInnerXml()
        else:
            productSpec["mrpPrice"] = ""

        if len(self.browser.findElement(
                'div[class="title-wrap line fk-font-family-museo section omniture-field"]>h1[class="title"]')) > 0:
            productSpec["name"] = self.browser.findElement(
                'div[class="title-wrap line fk-font-family-museo section omniture-field"]>h1[class="title"]')[ \
                0].toInnerXml()
        else:
            productSpec["name"] = ""

        if len(self.browser.findElement(
                'div[class="title-wrap line fk-font-family-museo section omniture-field"]>span[class="subtitle"]')) > 0:
            productSpec["color"] = self.browser.findElement(
                'div[class="title-wrap line fk-font-family-museo section omniture-field"]>span[class="subtitle"]')[ \
                0].toInnerXml()
        else:
            productSpec["color"] = ""

        # spec scrapping
        for t in self.browser.findElement('table[class="specTable"]>tbody'):
            specHeader = t.findAll('tr>th')[0].toInnerXml().strip().lower()
            for td in t.findAll('tr>td'):
                if td.attribute("class") == "specsKey":
                    specKey = td.toInnerXml().strip()
                else:
                    specVal = td.toInnerXml().strip().replace("\n", "")
                    productSpec[specHeader + "." + specKey] = specVal

        # collect image links

        for e in self.browser.findElement('div[class="imgWrapper"]>img'):
            if e.attribute('data-zoomimage') == "":
                listOfPicUrls.append(e.attribute('data-src'))
            else:
                listOfPicUrls.append(e.attribute('data-zoomimage'))

        return [json.dumps(productSpec), listOfPicUrls]


def validateData(self, productSpecJson, listOfPicUrls):
    productSpec = json.loads(productSpecJson)
    if len(productSpec) == 0:
        return False
    if productSpec["name"] == "":
        return False
    if len(listOfPicUrls) == 0:
        return False
    return True






