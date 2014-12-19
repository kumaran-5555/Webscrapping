#!/usr/bin/python
__author__ = 'serajago'

import scrapperJob


class unitTestScrapperJob(scrapperJob.ScrapperJob):
    def __init__(self):

        super().__init__()

    def collectData(self, seed):
        return ["d1|d2|d3", ["s1", "s2"]]

    def validateData(self, dataString, listOfSeeds):
        return True


job = unitTestScrapperJob()

job.initScrapperJob("mobiles_home_seed", "mobile_brands_seed", "Mobile brands", database="project005_scrapping_20141216")

job.startJob()