
from jira.jiraRequests.issues import getAllIssues, getIssuesInSprintWithUpdatedAfter, getIssuesNotInAnySprintWithUpdatedAfter
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
from config import config
from db.sqlite3.connector import SqliteConnector
import concurrent.futures
from functools import partial

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
    

def processSprintPerBoard(responseProcessor, updatedAt, boardId):
    # each thread should have its db connection
    dbFile = config["dbFile"]
    dbConnector = SqliteConnector(dbFile)
    print("Processing on board id:", boardId)
    response = getAllSprintsInBoard(boardId)
    dbReadyDataForSprint = sprint.update(dbConnector, responseProcessor, response, {"boardId":boardId})
    for sprintData in dbReadyDataForSprint:
        response = getIssuesInSprintWithUpdatedAfter(sprintData["id"], updatedAt)
        sprintIssueLink.update(dbConnector, responseProcessor, response, {"sprintId":sprintData["id"]})
        issue.update(dbConnector,responseProcessor, response)
    return boardId

# @param: updatedAt
#   will update those issues created or updated after a certain date(inclusive)
#   format yyyy-mm-dd (ex)2020-01-01
#   this param only affects issue update
#   cf) the first issue was created at 2014-06-17
def update(dbConnector, responseProcessor, updatedAt = "2014-06-17"): 

    print("update boards data")
    response = getAllBoards()
    dbReadyData = board.update(dbConnector, responseProcessor, response)
    
    # Non-concurrent version
    # print("update sprint data and related issue data since", updatedAt)
    # for boardData in dbReadyData:
    #     response = getAllSprintsInBoard(boardData["id"])
    #     dbReadyDataForSprint = sprint.update(dbConnector, responseProcessor, response, {"boardId":boardData["id"]})

    #     for sprintData in dbReadyDataForSprint:
    #         response = getIssuesInSprintWithUpdatedAfter(sprintData["id"], updatedAt)
    #         sprintIssueLink.update(dbConnector, responseProcessor, response, {"sprintId":sprintData["id"]})
    #         issue.update(dbConnector,responseProcessor, response)

    # Multithread version
    print("update sprint data and related issue data since", updatedAt)
    boardIds = []
    for boardData in dbReadyData:
        boardIds.append(boardData["id"])

    partialProcessSprintPerBoard = partial(processSprintPerBoard, responseProcessor, updatedAt)
        
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor: #ProcessPoolExecutor(max_workers=2)
        # Start the load operations and mark each future with its URL
        for id in executor.map(partialProcessSprintPerBoard, boardIds):
            print("Board Done:", id)

    print("update issue data not included in sprint since", updatedAt)
    response = getIssuesNotInAnySprintWithUpdatedAfter(updatedAt)
    issue.update(dbConnector,responseProcessor, response)
    
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
    
    



    # not being used
    # sprintRecordList, sprintIssueLinkRecordList = processSprint(response)
    # dbConnector.insertRecords(sprint.model, sprintRecordList)
    # dbConnector.insertRecords(sprintIssueLink.model, sprintIssueLinkRecordList)