from db.sqlite3.connector import SqliteConnector
import pandas as pd

def getIssueBySprintId(ClassDbConnector, sprintId):
    dbConnector = ClassDbConnector()
    selectedFields = ["Sprint.id as sprintId", "Sprint.name as sprint", 
                    "Issue.id as issueId", "Issue.key as issueKey", "Issue.storyPoints", 
                    "IssueType.name as issueType", "Status.name as status", "Priority.name as priority",
                    "Issue.created", "Issue.updated", "Issue.resolutionDate","Resolution.name as resolution",
                    "Issue.creatorName", "Issue.reporterName", "Issue.assigneeName"]
    joinClauses = [
        {"type":"LEFT", "tableName":"IssueType", "onClause":"Issue.issueTypeId = IssueType.id"},
        {"type":"LEFT", "tableName":"Status", "onClause":"Issue.statusId = Status.id"},
        {"type":"LEFT", "tableName":"Priority", "onClause":"Issue.priorityId = Priority.id"},
        {"type":"LEFT", "tableName":"Resolution", "onClause":"Issue.resolutionId = Resolution.id"},
        {"type":"LEFT", "tableName":"SprintIssueLink", "onClause":"Issue.id = SprintIssueLink.issueId"},
        {"type":"LEFT", "tableName":"Sprint", "onClause":"Sprint.id = SprintIssueLink.sprintId"} 
    ]
    whereClause = None
    if sprintId != "*":
        whereClause = "Sprint.id = '{}'".format(sprintId)
    statement = dbConnector.queryFromJoinStatement(selectedFields,"Issue",joinClauses,whereClause)
    df = pd.read_sql_query(statement, dbConnector.connection)
    return df

def getIssueById(ClassDbConnector, issueId): # * for all sprint
    dbConnector = ClassDbConnector()
    selectedFields = ["Issue.id", "Issue.key", "Issue.storyPoints", 
                    "IssueType.name as issueType", "Status.name as status", "Priority.name as priority",
                    "Issue.created", "Issue.updated", "Issue.resolutionDate","Resolution.name as resolution",
                    "Issue.creatorName", "Issue.reporterName", "Issue.assigneeName"]
    joinClauses = [
        {"type":"LEFT", "tableName":"IssueType", "onClause":"Issue.issueTypeId = IssueType.id"},
        {"type":"LEFT", "tableName":"Status", "onClause":"Issue.statusId = Status.id"},
        {"type":"LEFT", "tableName":"Priority", "onClause":"Issue.priorityId = Priority.id"},
        {"type":"LEFT", "tableName":"Resolution", "onClause":"Issue.resolutionId = Resolution.id"}        
    ]
    whereClause = None
    if issueId != "*":
        whereClause = "Issue.id = '{}'".format(issueId)
    statement = dbConnector.queryFromJoinStatement(selectedFields,"Issue",joinClauses,whereClause)
    df = pd.read_sql_query(statement, dbConnector.connection)
    return df


def getSprintByBoardId(ClassDbConnector, boardId):
    dbConnector = ClassDbConnector()
    selectedFields = ["Board.id as boardId", "Board.name as boardName", 
                        "Sprint.id as sprintId", "Sprint.name as sprintName", 
                        "Sprint.state as sprintState", "Sprint.startDate", 
                        "Sprint.endDate", "Sprint.completeDate"]
    joinClauses = [
        {"type":"LEFT", "tableName":"Board", "onClause":"Board.id = Sprint.boardId"}
    ]
    whereClause = None
    if boardId != "*":
        whereClause = "Board.id = '{}'".format(boardId)
    statement = dbConnector.queryFromJoinStatement(selectedFields,"Sprint",joinClauses,whereClause)
    df = pd.read_sql_query(statement, dbConnector.connection)
    return df   

def getSprintById(ClassDbConnector, sprintId): # * for all sprint
    dbConnector = ClassDbConnector()
    selectedFields = ["Sprint.id as sprintId", "Sprint.name as sprintName", 
                        "Sprint.state as sprintState", "Sprint.startDate", 
                        "Sprint.endDate", "Sprint.completeDate"]
    whereClause = None
    if sprintId != "*":
        whereClause = "Sprint.id = '{}'".format(sprintId)
    statement = dbConnector.queryTableStatement(selectedFields,"Sprint",whereClause)
    df = pd.read_sql_query(statement, dbConnector.connection)
    return df    

def getBoardById(ClassDbConnector, boardId): # * for all board
    dbConnector = ClassDbConnector()
    selectedFields = ["Board.id", "Board.name", "Board.type"]
    whereClause = None
    if boardId != "*":
        whereClause = "Board.id = '{}'".format(boardId)
    statement = dbConnector.queryTableStatement(selectedFields,"Board",whereClause)
    df = pd.read_sql_query(statement, dbConnector.connection)
    return df

def getProjectById(ClassDbConnector, projectId):
    dbConnector = ClassDbConnector()
    selectedFields = ["Project.id", "Project.key", "Project.name", "Project.style"]
    whereClause = None
    if projectId != "*":
        whereClause = "Project.id = '{}'".format(projectId)
    statement = dbConnector.queryTableStatement(selectedFields,"Project",whereClause)
    df = pd.read_sql_query(statement, dbConnector.connection)
    return df