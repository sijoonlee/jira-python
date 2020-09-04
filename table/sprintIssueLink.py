model = {
    "name" : "SprintIssueLink",
    "fields" : [
        {"name" : "sprintId", "type" : "TEXT" },
        {"name" : "issueId", "type" : "TEXT" }
    ],
    "primaryKeys" : [ "sprintId", "issueId" ]#,
    # "foreignKeys" : [
    #     {"name": "sprintId", "references": "Sprint(id)"},
    #     {"name": "issueId", "references": "Issue(id)"},
    # ]
}

lookup = {
    "issueId":"id"
}
# sprintId will be inserted in other way since our response(getAllIssuesInSprint) doesn't have sprint information
# check update method in dbActions under businessLogic

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