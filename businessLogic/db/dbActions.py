
from jira.jiraRequests.issues import getAllIssues
from jira.jiraRequests.issueTypes import getIssueTypes
from jira.jiraRequests.priorities import getPriorities
from jira.jiraRequests.projects import getAllProjects
from jira.jiraRequests.statuses import getStatuses
from jira.jiraRequests.users import getAllUsers
from jira.jiraRequests.boards import getAllBoards
from jira.jiraRequests.sprints import getAllSprintsInBoard
from jira.jiraRequests.issuesInSprint import getAllIssuesInSprint
from jira.jiraRequests.processResponse import processResponse
from model import issue, priority, project, status, issueType, user, sprint, sprintIssueLink, board

def reset(dbConnector):
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

def update(dbConnector):

    response = getAllBoards()
    dbReadyData = processResponse(board.lookup, response)
    dbConnector.insertRecords(board.model, dbReadyData)

    for boardData in dbReadyData:
        response = getAllSprintsInBoard(boardData["id"])
        dbReadyDataForSprint = processResponse(sprint.lookup, response)
        dbConnector.insertRecords(sprint.model, dbReadyDataForSprint)

        for sprintData in dbReadyDataForSprint:
            response = getAllIssuesInSprint(boardData["id"],sprintData["id"])
            dbReadyDataForSprintIssueLink = processResponse(sprintIssueLink.lookup, response)
            for entity in dbReadyDataForSprintIssueLink:
                entity["sprintId"] = sprintData["id"]
            dbConnector.insertRecords(sprintIssueLink.model, dbReadyDataForSprintIssueLink)

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

    # not being used
    # sprintRecordList, sprintIssueLinkRecordList = processSprint(response)
    # dbConnector.insertRecords(sprint.model, sprintRecordList)
    # dbConnector.insertRecords(sprintIssueLink.model, sprintIssueLinkRecordList)