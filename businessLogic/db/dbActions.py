
from jira.jiraRequests.issues import getAllIssues
from jira.jiraRequests.issueTypes import getIssueTypes
from jira.jiraRequests.priorities import getPriorities
from jira.jiraRequests.projects import getAllProjects
from jira.jiraRequests.statuses import getStatuses
from jira.jiraRequests.users import getAllUsers
from jira.jiraRequests.boards import getAllBoards
from jira.jiraRequests.sprints import getAllSprintsInBoard
from jira.jiraRequests.issuesInSprint import getAllIssuesInSprint
from jira.jiraRequests.resolutions import getResolutions
from table import issue, priority, project, status, issueType, user, sprint, sprintIssueLink, board, resolution

def reset(dbConnector):

    issue.drop(dbConnector)
    priority.drop(dbConnector)
    project.drop(dbConnector)
    status.drop(dbConnector)
    issueType.drop(dbConnector)
    user.drop(dbConnector)
    sprint.drop(dbConnector)
    sprintIssueLink.drop(dbConnector)
    board.drop(dbConnector)
    resolution.drop(dbConnector)
    
    issue.create(dbConnector)
    priority.create(dbConnector)
    project.create(dbConnector)
    status.create(dbConnector)
    issueType.create(dbConnector)
    user.create(dbConnector)
    sprint.create(dbConnector)
    sprintIssueLink.create(dbConnector)
    board.create(dbConnector)
    resolution.create(dbConnector)
    

def update(dbConnector, responseProcessor):

    print("update boards data")
    response = getAllBoards()
    #dbReadyData = responseProcessor(board.lookup,response)
    dbReadyData = board.update(dbConnector, responseProcessor, response)
    
    print("update sprint data")
    for boardData in dbReadyData:
        response = getAllSprintsInBoard(boardData["id"])
        dbReadyDataForSprint = sprint.update(dbConnector, responseProcessor, response, {"boardId":boardData["id"]})

        for sprintData in dbReadyDataForSprint:
            response = getAllIssuesInSprint(boardData["id"],sprintData["id"])
            sprintIssueLink.update(dbConnector, responseProcessor, response, {"sprintId":sprintData["id"]})

    print("update user data")
    response = getAllUsers()
    user.update(dbConnector, responseProcessor, response)

    print("update resolution data")
    response = getResolutions()
    resolution.update(dbConnector, responseProcessor, response)

    print("update project data")
    response = getAllProjects()
    project.update(dbConnector, responseProcessor, response)

    print("update priority data")
    response = getPriorities()
    priority.update(dbConnector,responseProcessor, response)
    
    print("update status data")
    response = getStatuses()
    status.update(dbConnector,responseProcessor, response)
        
    print("update issueType data")
    response = getIssueTypes()
    issueType.update(dbConnector,responseProcessor, response)
    
    print("update issue data")
    response = getAllIssues()
    issue.update(dbConnector,responseProcessor, response)

    # not being used
    # sprintRecordList, sprintIssueLinkRecordList = processSprint(response)
    # dbConnector.insertRecords(sprint.model, sprintRecordList)
    # dbConnector.insertRecords(sprintIssueLink.model, sprintIssueLinkRecordList)