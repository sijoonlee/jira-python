model = {
    "name" : "Board",
    "fields" : [
        { "name": "id", "type": "TEXT", "option" : "PRIMARY KEY" },
        { "name": "name" , "type": "TEXT"},
        { "name": "type", "type": "TEXT"},
        { "name": "projectId", "type": "TEXT"}
    ]
}

# Lookup table
# @key : Field name in Database
# @value: Field path in Jira response's json structure
lookup = {
    "id" : "id",
    "name" : "name",
    "type" : "type",
    "projectId" : "location->projectId"
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