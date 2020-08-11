from db.sqlite3.connector import SqliteConnector
from jiraRequests.processResponse import processResponse
from utils.jsonUtil import readFileReport, writeFileReport
from model import issue, issueType, priority, project, status, user

def func(**args):
    print(args.items())



if __name__=="__main__":
    # data = {"a":"A", "b":"B"}
    # func(**data)

    # abc = "a->b->c"
    # print(abc.split("->"))
    dbFile = './db/sqlite3/storage/db.sqlite'
    dbConnector = SqliteConnector(dbFile)
    
    dbConnector.dropTable(issueType.model)
    dbConnector.dropTable(user.model)
    dbConnector.dropTable(priority.model)
    dbConnector.dropTable(status.model)
    dbConnector.dropTable(project.model)
    dbConnector.dropTable(issue.model)
    
    dbConnector.createTable(user.model)
    dbConnector.createTable(priority.model)
    dbConnector.createTable(project.model)
    dbConnector.createTable(status.model)
    dbConnector.createTable(issueType.model)
    dbConnector.createTable(issue.model)

    response = readFileReport("./exampleResponse/getAllProjects.json")
    dbReadyData = processResponse(project.lookup, response)
    dbConnector.insertRecords(project.model, dbReadyData)

    response = readFileReport("./exampleResponse/getAllIssues.json")
    dbReadyData = processResponse(issue.lookup, response)
    dbConnector.insertRecords(issue.model, dbReadyData)

    response = readFileReport("./exampleResponse/getAllUsers.json")
    dbReadyData = processResponse(user.lookup, response)
    dbConnector.insertRecords(user.model, dbReadyData)

    response = readFileReport("./exampleResponse/getIssueTypes.json")
    dbReadyData = processResponse(issueType.lookup, response)
    dbConnector.insertRecords(issueType.model, dbReadyData)

    response = readFileReport("./exampleResponse/getPriorities.json")
    dbReadyData = processResponse(priority.lookup, response)
    dbConnector.insertRecords(priority.model, dbReadyData)

    response = readFileReport("./exampleResponse/getStatuses.json")
    dbReadyData = processResponse(status.lookup, response)
    dbConnector.insertRecords(status.model, dbReadyData)
