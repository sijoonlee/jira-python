# https://docs.python.org/3/library/queue.html
# https://stackoverflow.com/questions/19369724/the-right-way-to-limit-maximum-number-of-threads-running-at-once
# https://stackoverflow.com/questions/45169559/how-to-make-worker-threads-quit-after-work-is-finished-in-a-multithreaded-produc
# https://docs.python.org/3.7/library/concurrent.futures.html#threadpoolexecutor



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
from db.sqlite3.connector import SqliteConnector
from jira.jiraRequests.responseProcessor import responseProcessor
import time
import concurrent.futures


def configureProcessSprintPerBoard(updatedAt):
    def processSprintPerBoard(boardId):
        # each thread should have its db connection
        dbFile = './db/sqlite3/storage/db.test.sqlite'
        dbConnector = SqliteConnector(dbFile)
        print("Processing on board id:", boardId)
        response = getAllSprintsInBoard(boardId)
        dbReadyDataForSprint = sprint.update(dbConnector, responseProcessor, response, {"boardId":boardId})
        print("# of Sprints",len(dbReadyDataForSprint))
        for sprintData in dbReadyDataForSprint:
            response = getIssuesInSprintWithUpdatedAfter(sprintData["id"], updatedAt)
            sprintIssueLink.update(dbConnector, responseProcessor, response, {"sprintId":sprintData["id"]})
            issue.update(dbConnector,responseProcessor, response)
        return boardId
    return processSprintPerBoard


if __name__=="__main__":
    dbFile = './db/sqlite3/storage/db.test.sqlite'
    dbConnector = SqliteConnector(dbFile)
    board.drop(dbConnector)
    sprint.drop(dbConnector)
    issue.drop(dbConnector)
    sprintIssueLink.drop(dbConnector)
    board.create(dbConnector)
    sprint.create(dbConnector)
    issue.create(dbConnector)
    sprintIssueLink.create(dbConnector)
    
    print("update boards data")
    response = getAllBoards()
    dbReadyData = board.update(dbConnector, responseProcessor, response)

    updatedAt = "2020-01-01"
    processSprintPerBoard = configureProcessSprintPerBoard(updatedAt)

    print("update sprint data and related issue data")
    boardIds = []
    for boardData in dbReadyData:
        boardIds.append(boardData["id"])
    print(boardIds)
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor: #ProcessPoolExecutor(max_workers=2)
        # Start the load operations and mark each future with its URL
        for id in executor.map(processSprintPerBoard, boardIds):
            print("Done:", id)


    duration = time.time() - start_time 
    # 2 workers = 487.64933943748474
    # 4 = 334.1659185886383
   
    print(duration)
    