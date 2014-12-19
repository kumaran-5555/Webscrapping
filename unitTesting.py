#!/usr/bin/python
__author__ = 'serajago'

import scrapperJob


class unitTestScrapperJob(scrapperJob.ScrapperJob):
    def __init__(self, inputSeedTableName, outputSeedTable, jobName, optionalParameters={},
                 emptyOutputTable=True, maxRetryAttempts=5, minSuccessPercentage=1):

        super().__init__(inputSeedTableName, outputSeedTable, jobName, optionalParameters=optionalParameters,
                         emptyOutputTable=emptyOutputTable, maxRetryAttempts=maxRetryAttempts,
                         minSuccessPercentage=minSuccessPercentage)

    def collectData(self, seed):
        return ["d1|d2|d3", ["s1", "s2"]]

    def validateData(self, dataString, listOfSeeds):
        return True


job = unitTestScrapperJob("mobiles_home_seed", "mobile_brands_seed", "Mobile brands")

job.initScrapperJob(database="project005_scrapping_20141216")

job.startJob()