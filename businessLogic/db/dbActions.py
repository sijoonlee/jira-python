from jira.jiraRequests.issues import getIssues, getIssuesInSprintWithUpdatedAfter, getIssuesNotInAnySprintWithUpdatedAfter, getIssuesMultiThread
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
import concurrent.futures
from functools import partial
from db.postgres.connector import PostgresConnector
from db.sqlite3.connector import SqliteConnector


class DbActions(object):
    def __init__(self, ClassDbConnector, responseProcessor, maxWorkers=4):
        self.ClassDbConnector = ClassDbConnector
        self.responseProcessor = responseProcessor
        self.maxWorkers = maxWorkers
        
    def reset(self):
        dbConnector = self.ClassDbConnector()

        sprintIssueLink.drop(dbConnector)
        issue.drop(dbConnector)
        sprint.drop(dbConnector)
        user.drop(dbConnector)
        resolution.drop(dbConnector)
        issueType.drop(dbConnector)
        status.drop(dbConnector)
        project.drop(dbConnector)
        priority.drop(dbConnector)
        board.drop(dbConnector)
        
        board.create(dbConnector)
        priority.create(dbConnector)
        project.create(dbConnector)
        status.create(dbConnector)
        issueType.create(dbConnector)
        resolution.create(dbConnector)
        user.create(dbConnector)
        sprint.create(dbConnector)
        issue.create(dbConnector)
        sprintIssueLink.create(dbConnector)    

    def processSprintPerBoardUsingAgileApi(self, boardId):
        # each thread should have its db connection
        dbConnector = self.ClassDbConnector()
        print("Processing on board id:", boardId)
        response = getAllSprintsInBoard(boardId)

        dbReadyDataForSprint = sprint.update(dbConnector, self.responseProcessor, response, {"boardId":boardId})
        for sprintData in dbReadyDataForSprint:
            response = getAllIssuesInSprint(boardId, sprintData["id"])
            issue.update(dbConnector, self.responseProcessor, response)
            sprintIssueLink.update(dbConnector, self.responseProcessor, response, {"sprintId":sprintData["id"]})
        return boardId

    def processSprintPerBoard(self, updatedAt, boardId):
        # each thread should have its db connection
        # dbConnector = self.ClassDbConnector()
        print("Processing on board id:", boardId)
        response = getAllSprintsInBoard(boardId)
        # dbReadyDataForSprint = sprint.update(SqliteConnector(), self.responseProcessor, response, {"boardId":boardId})
        dbReadyDataSprint = sprint.getDbReadyData(self.responseProcessor, response, {"boardId":boardId})
        dbReadyDataIssue = []
        dbReadySprintIssueLink = []
        for sprintData in dbReadyDataSprint:
            response = getIssuesInSprintWithUpdatedAfter(sprintData["id"], updatedAt)
            # issue.update(SqliteConnector(), self.responseProcessor, response)
            dbReadyDataIssue = [ *dbReadyDataIssue, *issue.getDbReadyData(self.responseProcessor, response) ]
            # sprintIssueLink.update(SqliteConnector(), self.responseProcessor, response, {"sprintId":sprintData["id"]})
            dbReadySprintIssueLink = [ *dbReadySprintIssueLink,\
                *sprintIssueLink.getDbReadyData(self.responseProcessor, response, {"sprintId":sprintData["id"]})]
            
        return dbReadyDataSprint, dbReadyDataIssue, dbReadySprintIssueLink

    # @param: updatedAt
    #   will update those issues created or updated after a certain date(inclusive)
    #   format yyyy-mm-dd (ex)2020-01-01
    #   this param only affects issue update
    #   cf) the first issue was created at 2014-06-17
    def update(self, updatedAt = "2014-06-17"): 
        dbConnector = self.ClassDbConnector()

        print("update user data")
        response = getAllUsers()
        user.update(dbConnector, self.responseProcessor, response)

        print("update resolution data")
        response = getResolutions()
        resolution.update(dbConnector, self.responseProcessor, response)

        print("update project data")
        response = getAllProjects()
        project.update(dbConnector, self.responseProcessor, response)

        print("update priority data")
        response = getPriorities()
        priority.update(dbConnector,self.responseProcessor, response)
        
        print("update status data")
        response = getStatuses()
        status.update(dbConnector,self.responseProcessor, response)
            
        print("update issueType data")
        response = getIssueTypes()
        issueType.update(dbConnector,self.responseProcessor, response)



        print("update boards data")
        response = getAllBoards()
        dbReadyData = board.update(dbConnector, self.responseProcessor, response)
        
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

        partialProcessSprintPerBoard = partial(self.processSprintPerBoard, updatedAt)
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.maxWorkers) as executor: #ProcessPoolExecutor(max_workers=2)
            # Start the load operations and mark each future with its URL
            for (dbReadyDataSprint, dbReadyDataIssue, dbReadySprintIssueLink) in executor.map(partialProcessSprintPerBoard, boardIds):
                sprint.updateUsingDbReadyData(dbConnector, dbReadyDataSprint)
                issue.updateUsingDbReadyData(dbConnector, dbReadyDataIssue)
                sprintIssueLink.updateUsingDbReadyData(dbConnector, dbReadySprintIssueLink)

        print("update issue data not included in sprint since", updatedAt)
        response = getIssuesNotInAnySprintWithUpdatedAfter(self.maxWorkers, updatedAt)
        issue.update(dbConnector,self.responseProcessor, response)
              
        
    def updateUsingAgileApi(self, maxWorkers = 10): 
        dbConnector = self.ClassDbConnector()
        
        print("update user data")
        response = getAllUsers()
        user.update(dbConnector, self.responseProcessor, response)

        print("update resolution data")
        response = getResolutions()
        resolution.update(dbConnector, self.responseProcessor, response)

        print("update project data")
        response = getAllProjects()
        project.update(dbConnector, self.responseProcessor, response)

        print("update priority data")
        response = getPriorities()
        priority.update(dbConnector, self.responseProcessor, response)
        
        print("update status data")
        response = getStatuses()
        status.update(dbConnector, self.responseProcessor, response)
            
        print("update issueType data")
        response = getIssueTypes()
        issueType.update(dbConnector, self.responseProcessor, response)

        print("update boards data")
        response = getAllBoards()
        dbReadyData = board.update(dbConnector, self.responseProcessor, response)
        
        # Multithread version
        print("update sprint data and related issue data since")
        boardIds = []
        for boardData in dbReadyData:
            boardIds.append(boardData["id"])

        partialProcessSprintPerBoardUsingAgileApi = partial(self.processSprintPerBoardUsingAgileApi, self.ClassDbConnector)
            
        with concurrent.futures.ThreadPoolExecutor(max_workers= self.maxWorkers) as executor: #ProcessPoolExecutor(max_workers)
            # Start the load operations and mark each future with its URL
            for id in executor.map(partialProcessSprintPerBoardUsingAgileApi, boardIds):
                print("Board Done:", id)

        print("update all issues")
        response = getIssuesMultiThread(self.maxWorkers)
        issue.update(dbConnector, self.responseProcessor, response)

        
        

