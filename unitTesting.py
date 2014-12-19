#!/usr/bin/python
__author__ = 'serajago'


import scrapperJob

job = scrapperJob.ScrapperJob(inputSeedTableName="mobiles_home_seed", jobName="Mobile brands", outputSeedTable="mobile_brands_seed")


job.initScrapperJob(database="project005_scrapping_20141216")


job.startJob()