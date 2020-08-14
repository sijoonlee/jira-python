model = {
    "name": "Resolution",
    "fields": [
        {"name": "id", "type": "TEXT", "option": "PRIMARY KEY"},
        {"name": "name", "type": "TEXT"},
        {"name": "description", "type": "TEXT"}
    ]   
}

# Lookup table
# @key : Field name in Database
# @value: Field path in Jira response's json structure
lookup = {
    "id" : "id",
    "name" : "name",
    "description" : "description"
}

def drop(dbConnector):
    dbConnector.dropTable(model)

def create(dbConnector):
    dbConnector.createTable(model)

def update(dbConnector, responseProcessor, response, injection={}):
    dbReadyData = responseProcessor(lookup, response, injection)
    dbConnector.insertRecords(model, dbReadyData)
    return dbReadyData