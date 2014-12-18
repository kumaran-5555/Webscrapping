__author__ = 'serajago'

import mysql.connector
import webkitBrowser


class ScrapperJob():
    def __init__(self, inputSeedTableName, outputSeedTable, version, dictionaryOfOptionalParameter={},
                 emptyOutputTable=True, maxRetryAttempts=5, minSuccessPercentage=0.95):
        '''

        :param inputSeedTableName: name of the table which has seed to be processed
        :param outputSeedTable:  name of the table to store newly discovered seeds
        :param version: suffix for all tables - to identfy different scrapping iterations
        :param dictionaryOfOptionalParameter: optional parameter which can be access in all user defined methods
        :param emptyOutputTable: boolean to drop all rows in output table if exist during initDbConnection, if false, outputSeedTable is assumed to exist
        :param maxRetryAttempts: number of maximum retry attempts per input seed
        :param minSuccessPercentage: minimum percentage of seeds that have to be processed sucessfully to stop/retrying the job
        :return: nothing - expections are not handled
        '''
        self.optionalParamter = dictionaryOfOptionalParameter
        self.inputSeedTable = inputSeedTableName
        self.outputSeedTable = outputSeedTable
        self.version = version
        self.totalInputSeeds = 0
        self.totalOutputSeeds = 0
        self.totalSuccesses = 0
        self.empytOutputTable = emptyOutputTable
        self.maxRetryAttempts = maxRetryAttempts
        self.currentRetryAttempts = 0
        self.minSuccessPercentage = minSuccessPercentage
        self.browser = None
        self.dbObject = None
        self.dbCursor = None
        self.dbName = None
        self.createSeedTableQuery = """CREATE TABLE IF NOT EXISTS `{database}`.`{outputSeedTable}` (
            `seed` VARCHAR(1024) NULL,
            `seed_id` INT NOT NULL AUTO_INCREMENT,
            `parent_seed_table` VARCHAR(100) NULL,
            `parent_seed_id` INT NULL,
            `val` VARCHAR(4196) NULL,
            `status` VARCHAR(10) NULL DEFAULT 'NONE',
            `retry_count` INT NULL DEFAULT 0,
            `start_time` DATETIME NULL,
            `end_time` DATETIME NULL,
            PRIMARY KEY (`seed_id`))
            ENGINE = InnoDB;"""

        self.dropSeedTableQuery = "DROP TABLE IF EXISTS `{database}`.`{outputSeedTable}` ;"

        self.selectUnprocessedSeedsQuery = """SELECT seed, seed_id FROM `{database}`.`{inputSeedTable}`
            WHERE (status like 'NONE') or (status like 'FAILED' and retry_count < {maxRetryAttempts});"""

        self.updateInputSeedTableQuery = """UPDATE `{database}`.`{inputSeedTable}`
            SET val = {data}, status = {status}, start_time={startTime}, end_time={endTime}, retryCount = retryCount + 1
            WHERE seed_id == {seedId};"""

        self.insertOutputSeedTableQuery = """INSERT INTO `{database}`.`{outputSeedTable}`
            SET seed = {seed}, status = 'NONE', parent_seed_id = {parentSeedId}, parent_seed_table = {inputSeedTable};"""


    def initScrapperJob(self, gui=True, loadImages=False, javaScriptEnabled=False, host="kumaran-linux.cloudapp.net",
                        database="poject005-scrapper", user="project005", password="pivotproject005"):
        '''

        :param gui: boolean browser gui
        :param loadImages: boolean load images or not
        :param javaScriptEnabled: boolean javascript enabled or not
        :param host: host name of DB
        :param database: database of DB
        :param user: username of DB
        :param password: password of DB
        :return: nothing - exceptions are not handled
        :except: db connection related errors, browser initialization errors
        '''
        self.browser = webkitBrowser.Browser(gui=gui, loadImages=loadImages, javaScriptEnabled=javaScriptEnabled)
        self.dbObject = mysql.connector.connect(host=host, password=password, database=database, user=user)
        self.dbName = database
        self.dbCursor = self.dbObject.cursor()

        # check for input tables and output tables
        # if input table is not present raise exception
        # create output table if doesn't exist

        # create output table, drop if required
        if self.empytOutputTable:
            self.dbCursor.execute(self.dropSeedTableQuery.format(database=database,
                                                                 outputSeedTable=self.outputSeedTable))
            # create output table
            self.dbCursor.execute(
                self.createSeedTableQuery.format(database=database, outputSeedTable=self.outputSeedTable))

        def startJob(self):
            '''

            runs in loop as long as it finds any input seeds
            updates input and output seeds accordingly
            exits when minSuccessPercentage is met /no input seeds

            :return: nothing
            '''
            while True:
                self.se


        def collectData(self):
            '''
            will be called for each of unfinished/failed seeds

            user should implement this method
            load new seeds and collect data
            when returing multiple data, use | separation
            :return: return data and seeds collected from the current seed
            :rtype: list(data, listOfSeeds)
            '''

            return None

        def validateData(self, dataString, listOfSeeds):
            '''
            called after collectData() for each seed

            user should implement this method
            :param dataString: data collected from the current seed
            :param listOfSeeds: seeds collected from the current seed
            :return: true if validation succeeds, false if validation fails
            :rtype: bool
            '''






