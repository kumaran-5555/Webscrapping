__author__ = 'serajago'

import scrapperJob


class MobileBrandsJob(scrapperJob.ScrapperJob):
    def __init__(self):
        super().__init__()
        super().initScrapperJob("mobiles_home_seed", "mobiles_brands_seed", __name__, gui=True, javaScriptEnabled=True, database="project005_scrapping_20141216")

    def collectData(self, seed):
        data = "N/A"
        listOfSeeds = []

        self.browser.loadPage(self.browser.decodedUrl(seed))
        for e in self.browser.findElement('ul[id="brand"]>li'):
            listOfSeeds.append(e.attribute("title"))

        return [data, listOfSeeds]

    def validateData(self, dataString, listOfSeeds):
        if len(listOfSeeds) != 0:
            return True
        return False



