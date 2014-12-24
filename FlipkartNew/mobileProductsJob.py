__author__ = 'serajago'

import scrapperJob
import FlipkartNew.helperFunctions


class MobileProductsJob(scrapperJob.ScrapperJob):
    def __init__(self):
        super().__init__()
        super().initScrapperJob("mobiles_brands_seed", "mobiles_products_seed", __name__, gui=True,
                                javaScriptEnabled=True, database="project005_scrapping_20141216",
                                emptyOutputTable=False)

    def collectData(self, seed):
        '''

        :param seed:
        :return: [productCount, [listOfProductLinks]]
        '''
        productCount = 0
        listOfSeeds = []

        baseUrl = 'http://www.flipkart.com/mobiles/pr?sid=tyy,4io&otracker=nmenu_sub_electronics_0_All%20Brands'

        self.browser.loadPage(self.browser.decodedUrl(baseUrl))
        # select the brand
        self.browser.clickElement('ul[id="brand"]>li[title="' + seed + '"]>a')
        self.browser.waitSecs(5)

        # start scrolling it auto loads products
        sts = self.browser.scrollPageTill(FlipkartNew.helperFunctions.user_stopScrolling, maxTries=100, timerStep=750)
        if not sts:
            # return empty info and raise failed in validation
            return [0, []]

        # start clicking manually till all products are loaded
        sts = self.browser.clickElementTill('div[id="show-more-results"][style="display: block; "]',
                                            FlipkartNew.helperFunctions.user_stopClicking,
                                            afterClick=FlipkartNew.helperFunctions.user_afterClick, maxTries=20)
        if not sts:
            # return empty info and raise failed in validation
            return [0, []]

        # all products are loaded now

        # in stock products
        for p in self.browser.findElement('a[class="pu-image fk-product-thumb "]'):
            productCount += 1
            listOfSeeds.append(p.attribute("href"))
        # out of stock products
        for p in self.browser.findElement('a[class="pu-image fk-product-thumb oos"]'):
            productCount += 1
            listOfSeeds.append(p.attribute("href"))

        return [str(productCount), listOfSeeds]

    def validateData(self, dataString, listOfSeeds):
        if int(dataString) != 0:
            return True
        return False




