from db.sqlite3.connector import SqliteConnector
from model import issue, priority, project, status, issueType, user, sprint, sprintIssueLink
from jira.jiraRequests.issues import getAllIssues
from jira.jiraRequests.issueTypes import getIssueTypes
from jira.jiraRequests.priorities import getPriorities
from jira.jiraRequests.projects import getAllProjects
from jira.jiraRequests.statuses import getStatuses
from jira.jiraRequests.users import getAllUsers
from jira.jiraRequests.processResponse import processResponse
from jira.jiraRequests.processSprint import processSprint


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
    
    dbConnector.createTable(user.model)
    dbConnector.createTable(priority.model)
    dbConnector.createTable(project.model)
    dbConnector.createTable(status.model)
    dbConnector.createTable(issueType.model)
    dbConnector.createTable(issue.model)
    dbConnector.createTable(sprint.model)
    dbConnector.createTable(sprintIssueLink.model)


    response = getAllUsers()
    dbReadyData = processResponse(user.lookup, response)
    dbConnector.insertRecords(user.model, dbReadyData)

    response = getAllProjects()
    dbReadyData = processResponse(project.lookup, response)
    dbConnector.insertRecords(project.model, dbReadyData)

    response = getPriorities()
    dbReadyData = processResponse(priority.lookup, response)
    dbConnector.insertRecords(priority.model, dbReadyData)

    response = getStatuses()
    dbReadyData = processResponse(status.lookup, response)
    dbConnector.insertRecords(status.model, dbReadyData)
    
    response = getIssueTypes()
    dbReadyData = processResponse(issueType.lookup, response)
    dbConnector.insertRecords(issueType.model, dbReadyData)

    response = getAllIssues()
    dbReadyData = processResponse(issue.lookup, response)
    dbConnector.insertRecords(issue.model, dbReadyData)

    sprintRecordList, sprintIssueLinkRecordList = processSprint(response)
    dbConnector.insertRecords(sprint.model, sprintRecordList)
    dbConnector.insertRecords(sprintIssueLink.model, sprintIssueLinkRecordList)

    selectedFields = ["Project.key", "Issue.key", "Issue.reporterName", "Status.name"]
    joinClauses = [
        {"type":"LEFT", "tableName":"IssueType", "onClause":"Issue.issueTypeId = IssueType.id"},
        {"type":"LEFT", "tableName":"Project", "onClause":"Issue.projectId = Project.id"},
        {"type":"LEFT", "tableName":"Status", "onClause":"Issue.statusId = Status.id"},
        {"type":"LEFT", "tableName":"Priority", "onClause":"Issue.priorityId = Priority.id"}
    ]
    whereClause = 'Issue.projectId = "10000"'
    result = dbConnector.queryFromJoin(selectedFields, "Issue", joinClauses, whereClause)
    print(result)


    selectedFields = ["Sprint.name", "Issue.summary", "IssueType.name"]
    joinClauses = [
        {"type":"LEFT", "tableName":"Issue", "onClause":"Issue.id = SprintIssueLink.issueId"},
        {"type":"LEFT", "tableName":"Sprint", "onClause":"Sprint.id = SprintIssueLink.sprintId"},
        {"type":"LEFT", "tableName":"IssueType", "onClause":"Issue.issueTypeId = IssueType.id"}
    ]
    whereClause = 'Issue.projectId = "10000"'
    result = dbConnector.queryFromJoin(selectedFields, "SprintIssueLink", joinClauses, whereClause)
    print(result)