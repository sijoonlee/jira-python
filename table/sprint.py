model = {
    "name" : "Sprint",
    "fields" : [
        {"name" : "id", "type" : "TEXT", "option" : "PRIMARY KEY" },
        {"name" : "name", "type" : "TEXT" },
        {"name" : "goal", "type" : "TEXT" },
        {"name" : "state", "type" : "TEXT" },
        {"name" : "startDate", "type" : "TIMESTAMPTZ" },
        {"name" : "endDate", "type" : "TIMESTAMPTZ" },
        {"name" : "completeDate", "type" : "TIMESTAMPTZ" }
    ]#,
    # "foreignKeys" : [
    #     {"name": "boardId", "references": "Board(id)"}
    # ]
}

lookup = {
    "id":"id",
    "name":"name",
    "goal":"goal",
    "state":"state",
    "startDate":"startDate",
    "endDate":"endDate",
    "completeDate":"completeDate"
}

def drop(dbConnector):
    dbConnector.dropTable(model)

def create(dbConnector):
    dbConnector.createTable(model)

def update(dbConnector, responseProcessor, response, injection={}):
    dbReadyData = responseProcessor(lookup, response, injection)
    dbConnector.insertRecords(model, dbReadyData)
    return dbReadyData

def updateUsingDbReadyData(dbConnector, dbReadyData):
    dbConnector.insertRecords(model, dbReadyData)
    return dbReadyData

def getDbReadyData(responseProcessor, response, injection={}):
    return responseProcessor(lookup, response, injection)