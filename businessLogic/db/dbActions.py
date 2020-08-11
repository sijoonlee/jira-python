
from jiraRequests.issues import getAllIssues
from jiraRequests.issueTypes import getIssueTypes
from jiraRequests.priorities import getPriorities
from jiraRequests.projects import getAllProjects
from jiraRequests.statuses import getStatuses
from jiraRequests.users import getAllUsers
from jiraRequests.processResponse import processResponse
from jiraRequests.processSprint import processSprint
from model import issue, priority, project, status, issueType, user, sprint, sprintIssueLink

def reset(dbConnector):
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

def update(dbConnector):
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