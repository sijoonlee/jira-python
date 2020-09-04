model = {
    "name" : "BoardSprintLink",
    "fields" : [
        {"name" : "boardId", "type" : "TEXT" },
        {"name" : "sprintId", "type" : "TEXT" }
    ],
    "primaryKeys" : [ "boardId", "sprintId" ]#,
    # "foreignKeys" : [
    #     {"name": "sprintId", "references": "Sprint(id)"},
    #     {"name": "issueId", "references": "Issue(id)"},
    # ]
}

lookup = {
    "sprintId":"id"
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