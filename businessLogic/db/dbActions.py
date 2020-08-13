
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

    print("update boards data")
    response = getAllBoards()
    dbReadyData = processResponse(board.lookup, response)
    dbConnector.insertRecords(board.model, dbReadyData)

    print("update sprint data")
    for boardData in dbReadyData:
        response = getAllSprintsInBoard(boardData["id"])
        dbReadyDataForSprint = processResponse(sprint.lookup, response)
        for entity in dbReadyDataForSprint:
            entity["boardId"] = boardData["id"]
        dbConnector.insertRecords(sprint.model, dbReadyDataForSprint)

        for sprintData in dbReadyDataForSprint:
            response = getAllIssuesInSprint(boardData["id"],sprintData["id"])
            dbReadyDataForSprintIssueLink = processResponse(sprintIssueLink.lookup, response)
            for entity in dbReadyDataForSprintIssueLink:
                entity["sprintId"] = sprintData["id"]
            dbConnector.insertRecords(sprintIssueLink.model, dbReadyDataForSprintIssueLink)

    print("update user data")
    response = getAllUsers()
    dbReadyData = processResponse(user.lookup, response)
    dbConnector.insertRecords(user.model, dbReadyData)

    print("update project data")
    response = getAllProjects()
    dbReadyData = processResponse(project.lookup, response)
    dbConnector.insertRecords(project.model, dbReadyData)

    print("update priority data")
    response = getPriorities()
    dbReadyData = processResponse(priority.lookup, response)
    dbConnector.insertRecords(priority.model, dbReadyData)

    print("update status data")
    response = getStatuses()
    dbReadyData = processResponse(status.lookup, response)
    dbConnector.insertRecords(status.model, dbReadyData)
    
    print("update issueType data")
    response = getIssueTypes()
    dbReadyData = processResponse(issueType.lookup, response)
    dbConnector.insertRecords(issueType.model, dbReadyData)
    
    print("update issue data")
    response = getAllIssues()
    dbReadyData = processResponse(issue.lookup, response)
    dbConnector.insertRecords(issue.model, dbReadyData)

    # not being used
    # sprintRecordList, sprintIssueLinkRecordList = processSprint(response)
    # dbConnector.insertRecords(sprint.model, sprintRecordList)
    # dbConnector.insertRecords(sprintIssueLink.model, sprintIssueLinkRecordList)