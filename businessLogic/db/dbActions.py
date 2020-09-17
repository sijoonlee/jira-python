from jira.jiraRequests.issues import getIssues, getIssuesMultiThread, getIssuesInSprintWithUpdatedAfter
from jira.jiraRequests.issueTypes import getIssueTypes
from jira.jiraRequests.priorities import getPriorities
from jira.jiraRequests.projects import getAllProjects
from jira.jiraRequests.statuses import getStatuses
from jira.jiraRequests.users import getAllUsers
from jira.jiraRequests.boards import getAllBoards
from jira.jiraRequests.sprints import getAllSprintsInBoard
from jira.jiraRequests.issuesInSprint import getAllIssuesInSprint
from jira.jiraRequests.resolutions import getResolutions
from table import issue, priority, project, status, issueType, user, sprint, sprintIssueLink, board, resolution, boardSprintLink
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

        boardSprintLink.drop(dbConnector)
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
        boardSprintLink.create(dbConnector) 

    def processSprintPerBoard(self, boardId):
        response = getAllSprintsInBoard(boardId)
        dbReadyDataSprint = sprint.getDbReadyData(self.responseProcessor, response)
        dbReadyDataBoardSprintLink = boardSprintLink.getDbReadyData(self.responseProcessor, response, {"boardId":boardId})
        return dbReadyDataSprint, dbReadyDataBoardSprintLink

    def processIssuePerSprint(self, sprintId):
        dbReadyDataIssue = []
        dbReadySprintIssueLink = []
        response = getIssuesInSprintWithUpdatedAfter(sprintId, None)
        dbReadyDataIssue = issue.getDbReadyData(self.responseProcessor, response)
        dbReadySprintIssueLink = sprintIssueLink.getDbReadyData(self.responseProcessor, response, {"sprintId":sprintId})
        
        return dbReadyDataIssue, dbReadySprintIssueLink

    def update(self): 
        dbConnector = self.ClassDbConnector()

        print("fetch user data")
        responseUser = getAllUsers()
    
        print("fetch resolution data")
        responseResolution = getResolutions()
        
        print("fetch project data")
        responseProject = getAllProjects()
        
        print("fetch priority data")
        responsePriority = getPriorities()
                
        print("fetch status data")
        responseStatus = getStatuses()

        print("fetch issueType data")
        responseIssueType = getIssueTypes()
                
        print("fetch boards data")
        responseBoard = getAllBoards()
        dbReadyDataBoard = board.getDbReadyData(self.responseProcessor,responseBoard)

        # Multithread version
        # Collect data using multi-thread
        boardIds = []
        for boardData in dbReadyDataBoard:
            boardIds.append(boardData["id"])
        print("# of boards:", len(boardIds))

        print("fetch sprint data and its relation with board data(M:N)")
        CollectDbReadyDataSprint = []
        CollectDbReadyDataBoardSprintLink = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.maxWorkers) as executor:
            for (dbReadyDataSprint, dbReadyDataBoardSprintLink) in executor.map(self.processSprintPerBoard, boardIds):
                CollectDbReadyDataSprint = [*CollectDbReadyDataSprint, *dbReadyDataSprint]
                CollectDbReadyDataBoardSprintLink = [*CollectDbReadyDataBoardSprintLink, *dbReadyDataBoardSprintLink]
        
        # collect unique sprint ids
        sprintIds = set()
        for record in CollectDbReadyDataSprint:
            sprintIds.add(record["id"])
        print("# of sprints", len(sprintIds))
        sprintIds = list(sprintIds)

        print("fetch issue data that belong to sprints and its relation with sprint data(M:N)")
        CollectDbReadyDataIssue = []
        CollectDbReadySprintIssueLink = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.maxWorkers) as executor: #ProcessPoolExecutor(max_workers=2)
            for (dbReadyDataIssue, dbReadySprintIssueLink) in executor.map(self.processIssuePerSprint, sprintIds):
                CollectDbReadyDataSprint = [*CollectDbReadyDataSprint, *dbReadyDataSprint]
                CollectDbReadyDataBoardSprintLink = [*CollectDbReadyDataBoardSprintLink, *dbReadyDataBoardSprintLink]

                CollectDbReadyDataIssue = [*CollectDbReadyDataIssue, *dbReadyDataIssue]
                CollectDbReadySprintIssueLink = [*CollectDbReadySprintIssueLink, *dbReadySprintIssueLink]
        
        print("# of sprint-issue links", len(CollectDbReadySprintIssueLink))
        print("# of board-sprint links", len(CollectDbReadyDataBoardSprintLink))

        ## Below commented code is using JQL query to retrieve issues that don't belong to any sprints
        ## However, there's strange behaviour of Jira Cloud API
        ## When JQL is used, queries don't include issues from below projects
        ## - Analytics Team / Design Feedback / Marketing Design / Security / UX - Chrissy 
        # print("update issue data not included in sprint since", updatedAt)
        # response = getIssuesNotInAnySprintWithUpdatedAfter(self.maxWorkers, updatedAt)
        # issue.update(dbConnector,self.responseProcessor, response)

        print("fetch all issue data including those not in sprints")
        responseIssue = getIssuesMultiThread(self.maxWorkers)
        print("# of total issues", len(responseIssue))

        # Put data into DB after using multi-threading
        # this is to avoid conflicts of any database actions with multi-threading
        print('update table: user')
        user.update(dbConnector, self.responseProcessor, responseUser)

        print('update table: resolution')
        resolution.update(dbConnector, self.responseProcessor, responseResolution)

        print('update table: project')
        project.update(dbConnector, self.responseProcessor, responseProject)
        
        print('update table: priority')
        priority.update(dbConnector,self.responseProcessor, responsePriority)
        
        print('update table: status')
        status.update(dbConnector, self.responseProcessor, responseStatus)
        
        print('update table: issueType')
        issueType.update(dbConnector, self.responseProcessor, responseIssueType)
        
        print('update table: sprint')
        sprint.updateUsingDbReadyData(dbConnector, CollectDbReadyDataSprint)

        print('update table: board')
        board.updateUsingDbReadyData(dbConnector, dbReadyDataBoard)

        print('update table: issue(only related with Sprint)')
        issue.updateUsingDbReadyData(dbConnector, CollectDbReadyDataIssue)

        print('update table: sprintIssueLink')
        sprintIssueLink.updateUsingDbReadyData(dbConnector, CollectDbReadySprintIssueLink)

        print('update table: boardSprintLink')
        boardSprintLink.updateUsingDbReadyData(dbConnector, CollectDbReadyDataBoardSprintLink)

        print('update table: iussue(total)')
        issue.update(dbConnector, self.responseProcessor, responseIssue)
        