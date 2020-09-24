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
from table.issue import Issue
from table.priority import Priority
from table.project import Project
from table.status import Status
from table.issueType import IssueType
from table.user import User
from table.sprint import Sprint
from table.sprintIssueLink import SprintIssueLink
from table.board import Board
from table.resolution import Resolution
from table.boardSprintLink import BoardSprintLink
from config import config
import concurrent.futures

class DbActions(object):
    def __init__(self, ClassDbConnector, responseProcessor, maxWorkers=4):
        self.ClassDbConnector = ClassDbConnector
        self.responseProcessor = responseProcessor
        self.maxWorkers = maxWorkers
        
    def reset(self):
        dbConnector = self.ClassDbConnector()

        BoardSprintLink.drop(dbConnector)
        SprintIssueLink.drop(dbConnector)
        Issue.drop(dbConnector)
        Sprint.drop(dbConnector)
        User.drop(dbConnector)
        Resolution.drop(dbConnector)
        IssueType.drop(dbConnector)
        Status.drop(dbConnector)
        Project.drop(dbConnector)
        Priority.drop(dbConnector)
        Board.drop(dbConnector)
        
        Board.create(dbConnector)
        Priority.create(dbConnector)
        Project.create(dbConnector)
        Status.create(dbConnector)
        IssueType.create(dbConnector)
        Resolution.create(dbConnector)
        User.create(dbConnector)
        Sprint.create(dbConnector)
        Issue.create(dbConnector)
        SprintIssueLink.create(dbConnector)
        BoardSprintLink.create(dbConnector) 

    def processSprintPerBoard(self, boardId):
        response = getAllSprintsInBoard(boardId)
        dbReadyDataSprint = Sprint.getDbReadyData(self.responseProcessor, response)
        dbReadyDataBoardSprintLink = BoardSprintLink.getDbReadyData(self.responseProcessor, response, {"boardId":boardId})
        return dbReadyDataSprint, dbReadyDataBoardSprintLink

    def processIssuePerSprint(self, sprintId):
        dbReadyDataIssue = []
        dbReadySprintIssueLink = []
        response = getIssuesInSprintWithUpdatedAfter(sprintId, None)
        dbReadyDataIssue = Issue.getDbReadyData(self.responseProcessor, response)
        dbReadySprintIssueLink = SprintIssueLink.getDbReadyData(self.responseProcessor, response, {"sprintId":sprintId})
        
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
        dbReadyDataBoard = Board.getDbReadyData(self.responseProcessor,responseBoard)

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
        User.update(dbConnector, self.responseProcessor, responseUser)

        print('update table: resolution')
        Resolution.update(dbConnector, self.responseProcessor, responseResolution)

        print('update table: project')
        Project.update(dbConnector, self.responseProcessor, responseProject)
        
        print('update table: priority')
        Priority.update(dbConnector,self.responseProcessor, responsePriority)
        
        print('update table: status')
        Status.update(dbConnector, self.responseProcessor, responseStatus)
        
        print('update table: issueType')
        IssueType.update(dbConnector, self.responseProcessor, responseIssueType)
        
        print('update table: sprint')
        Sprint.updateUsingDbReadyData(dbConnector, CollectDbReadyDataSprint)

        print('update table: board')
        Board.updateUsingDbReadyData(dbConnector, dbReadyDataBoard)

        print('update table: issue(only related with Sprint)')
        Issue.updateUsingDbReadyData(dbConnector, CollectDbReadyDataIssue)

        print('update table: sprintIssueLink')
        SprintIssueLink.updateUsingDbReadyData(dbConnector, CollectDbReadySprintIssueLink)

        print('update table: boardSprintLink')
        BoardSprintLink.updateUsingDbReadyData(dbConnector, CollectDbReadyDataBoardSprintLink)

        print('update table: issue(total)')
        Issue.update(dbConnector, self.responseProcessor, responseIssue)
        