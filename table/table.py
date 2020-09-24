class Table(object):
    model = {}
    lookup = {}

    @classmethod
    def printModel(cls):
        print(cls.model)

    @classmethod
    def printLookup(cls):
        print(cls.lookup)

    @classmethod
    def drop(cls, dbConnector):
        dbConnector.dropTable(cls.model)

    @classmethod
    def create(cls, dbConnector):
        dbConnector.createTable(cls.model)

    @classmethod
    def update(cls, dbConnector, responseProcessor, response, injection={}):
        dbReadyData = responseProcessor(cls.lookup, response, injection)
        dbConnector.insertRecords(cls.model, dbReadyData)
        return dbReadyData

    @classmethod
    def updateUsingDbReadyData(cls, dbConnector, dbReadyData):
        dbConnector.insertRecords(cls.model, dbReadyData)
        return dbReadyData

    @classmethod
    def getDbReadyData(cls, responseProcessor, response, injection={}):
        return responseProcessor(cls.lookup, response, injection)