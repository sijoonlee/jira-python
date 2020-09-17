model = {
    "name" : "Users", # table name, 'user' is reserved name in Postgres
    "fields" : [
        {"name" : "accountId", "type" : "TEXT", "option" : "PRIMARY KEY" },
        {"name" : "accountType", "type" : "TEXT" },
        {"name" : "emailAddress", "type" : "TEXT" },
        {"name" : "displayName" , "type" : "TEXT" },
        {"name" : "active", "type" : "BOOLEAN"} # caution: SQLite doesn't have boolean 0(false), 1(true)
    ]
}


# Lookup table
# @key : Field name in Database
# @value: Field path in Jira response's json structure
lookup = {
    "accountId" : "accountId",
    "accountType" : "accountType",
    "emailAddress" : "emailAddress",
    "displayName" : "displayName",
    "active" : "active"
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