from db.sqlite3.connector import SqliteConnector
from jira.jiraRequests.responseProcessor import responseProcessor
from jira.jiraRequests.processSprint import processSprint
from utils.jsonUtil import readFileReport, writeFileReport
from table import issue, issueType, priority, project, status, user, sprint, sprintIssueLink, board



if __name__=="__main__":

    dbFile = './db/sqlite3/storage/db.sqlite'
    dbConnector = SqliteConnector(dbFile)
    
    dbConnector.dropTable(issueType.model)
    dbConnector.dropTable(user.model)
    dbConnector.dropTable(priority.model)
    dbConnector.dropTable(status.model)
    dbConnector.dropTable(project.model)
    dbConnector.dropTable(issue.model)
    dbConnector.dropTable(sprint.model)
    dbConnector.dropTable(sprintIssueLink.model)
    dbConnector.dropTable(board.model)
    
    dbConnector.createTable(user.model)
    dbConnector.createTable(priority.model)
    dbConnector.createTable(project.model)
    dbConnector.createTable(status.model)
    dbConnector.createTable(issueType.model)
    dbConnector.createTable(issue.model)
    dbConnector.createTable(sprint.model)
    dbConnector.createTable(sprintIssueLink.model)
    dbConnector.createTable(board.model)

    response = readFileReport("./exampleResponse/getAllProjects.json")
    dbReadyData = responseProcessor(project.lookup, response)
    dbConnector.insertRecords(project.model, dbReadyData)

    response = readFileReport("./exampleResponse/getAllIssues.json")
    dbReadyData = responseProcessor(issue.lookup, response)
    dbConnector.insertRecords(issue.model, dbReadyData)
    
    sprintRecordList, sprintIssueLinkRecordList = processSprint(response)
    
    dbConnector.insertRecords(sprint.model, sprintRecordList)
    dbConnector.insertRecords(sprintIssueLink.model, sprintIssueLinkRecordList)

    response = readFileReport("./exampleResponse/getAllUsers.json")
    dbReadyData = responseProcessor(user.lookup, response)
    dbConnector.insertRecords(user.model, dbReadyData)

    response = readFileReport("./exampleResponse/getIssueTypes.json")
    dbReadyData = responseProcessor(issueType.lookup, response)
    dbConnector.insertRecords(issueType.model, dbReadyData)

    response = readFileReport("./exampleResponse/getPriorities.json")
    dbReadyData = responseProcessor(priority.lookup, response)
    dbConnector.insertRecords(priority.model, dbReadyData)

    response = readFileReport("./exampleResponse/getStatuses.json")
    dbReadyData = responseProcessor(status.lookup, response)
    dbConnector.insertRecords(status.model, dbReadyData)
