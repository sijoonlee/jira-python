from db.sqlite3.connector import SqliteConnector
import pandas as pd
import datetime
from datetime import timezone

dbFile = './db/sqlite3/storage/db.sqlite'
dbConnector = SqliteConnector(dbFile)

def numberOfIssuesInSprint(sprintId):    
    selectedFields = ["Sprint.name as sprint", "Issue.key"]
    joinClauses = [
        {"type":"LEFT", "tableName":"Sprint", "onClause":"Sprint.id = SprintIssueLink.sprintId"},
        {"type":"LEFT", "tableName":"Board", "onClause":"Board.id = Sprint.boardId"},
        {"type":"LEFT", "tableName":"Issue", "onClause":"Issue.id = SprintIssueLink.issueId"}
    ]
    whereClause = "Sprint.id = '{}'".format(sprintId)
    statement = dbConnector.queryFromJoinStatement(selectedFields,"SprintIssueLink",joinClauses,whereClause)

    # load data
    df = pd.read_sql_query(statement, dbConnector.connection)
    print(df)
    print(df.groupby("sprint").count())


def issuesInSprintsStartedBetween(boardId, startStr, endStr): # format '2020-01-01'
    start = datetime.datetime.strptime(startStr,'%Y-%m-%d').replace(tzinfo=timezone.utc)
    end = datetime.datetime.strptime(endStr,'%Y-%m-%d').replace(tzinfo=timezone.utc)

    selectedFields = ["Sprint.name as sprint", "Sprint.startDate", "Issue.key", "Issue.storyPoints","IssueType.name as issueType", "Status.name as status"]
    joinClauses = [
        {"type":"LEFT", "tableName":"Sprint", "onClause":"Sprint.id = SprintIssueLink.sprintId"},
        {"type":"LEFT", "tableName":"Board", "onClause":"Board.id = Sprint.boardId"},
        {"type":"LEFT", "tableName":"Issue", "onClause":"Issue.id = SprintIssueLink.issueId"},
        {"type":"LEFT", "tableName":"IssueType", "onClause":"Issue.issueTypeId =IssueType.id"},
        {"type":"LEFT", "tableName":"Status", "onClause":"Issue.statusId = Status.id"},
    ]
    whereClause = "Board.id = '{}'".format(boardId)
    statement = dbConnector.queryFromJoinStatement(selectedFields,"SprintIssueLink",joinClauses,whereClause)

    # load data
    df = pd.read_sql_query(statement, dbConnector.connection)
    df = df.drop(df[df.startDate == "None"].index)
    df["storyPoints"] = df["storyPoints"].replace({"None":"0"})
    df["storyPoints"] = pd.to_numeric(df["storyPoints"])
    df["startDate"] = pd.to_datetime(df["startDate"])
    df = df[ (df["startDate"] >= start) & (df["startDate"]<=end) ]
    
    return df


def numberOfIssuesGroupBySprint(boardId, startStr, endStr):
    
    df = issuesInSprintsStartedBetween(boardId, startStr, endStr)
    
    # counting issues
    df = df.filter(["sprint"], axis=1)
    df["count"] = ""
    df = df.groupby("sprint").count()
    print(df)
    return df

def pivotSumStoryPoints(boardId, startStr, endStr):
    df = issuesInSprintsStartedBetween(boardId, startStr, endStr)
    # show issue type metrics
    df = df.filter(["sprint", "issueType", "storyPoints", "status"], axis=1)
    pivotted = pd.pivot_table(df, index=['sprint','issueType','status'], values='storyPoints', aggfunc = 'sum')
    print(pivotted)
    return pivotted

def pivotCountIssues(boardId, startStr, endStr):
    df = issuesInSprintsStartedBetween(boardId, startStr, endStr)
    df = df.filter(["sprint", "issueType", "key", "status"], axis=1)
    pivotted = pd.pivot_table(df, index=['sprint','issueType','status'], values='key', aggfunc = 'count')
    print(pivotted)

    # this is how to convert pivot_table to Dataframe
    # flattened = pd.DataFrame(y.to_records())
    # print(flattened)
    return pivotted
    
def calculateWorkDonePercentage(boardId, startStr, endStr):
    pivotted = pivotSumStoryPoints(boardId, startStr, endStr)
    flattened = pd.DataFrame(pivotted.to_records())
    flattened.groupby("status").sum()
    #workToDo = flattened[flattened["status"] == "Work To Do"]
    flattened = flattened.groupby("status").sum()

    flattened['Percentage'] = flattened['storyPoints']/flattened['storyPoints'].sum()*100

    print(flattened)