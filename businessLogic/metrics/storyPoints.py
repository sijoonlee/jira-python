from businessLogic.metrics.metricsFunctions import countByGroup, percentageByGroup
from db.sqlite3.connector import SqliteConnector
import pandas as pd
import datetime
from datetime import timezone
from config import config


def getMetricsPerProject(projectKey):
    dbConnector = SqliteConnector()
    selectedFields = ["Issue.key as issue", "Issue.storyPoints", "IssueType.name as issueType","Status.name as status", "Issue.assigneeName", "Issue.created"]
    joinClauses = [
        {"type":"LEFT", "tableName":"IssueType", "onClause":"Issue.issueTypeId = IssueType.id"},
        {"type":"LEFT", "tableName":"Project", "onClause":"Issue.projectId = Project.id"},
        {"type":"LEFT", "tableName":"Status", "onClause":"Issue.statusId = Status.id"}
    ]
    whereClause = "Project.key = '{}'".format(projectKey)
    statement = dbConnector.queryFromJoinStatement(selectedFields,"Issue",joinClauses,whereClause)

    # load data
    df = pd.read_sql_query(statement, dbConnector.connection)

    # drop data where story points are none
    df = df.drop(df[df.storyPoints == "None"].index)
    df["storyPoints"] = pd.to_numeric(df["storyPoints"])

    # show
    df_status = df.groupby("status").sum()
    print(df_status)

    # parse string to datetime
    df["created"] = pd.to_datetime(df["created"])

    # filter > 2020.1.1
    start = datetime.datetime(year=2020,month=5,day=11).replace(tzinfo=timezone.utc)
    df = df[df["created"] >= start]
    
    
    df1 = df.groupby("assigneeName").sum()
    print(df1)
    df2 = df.groupby("issueType").sum()
    print(df2)
    df = df.groupby("status").sum()
    
    #df = df.groupby("storyPoints").count()
    return df

def findIssuesCreatedBetween(projectKey, startStr, endStr):
    dbConnector = SqliteConnector()
    start = datetime.datetime.strptime(startStr,'%Y-%m-%d').replace(tzinfo=timezone.utc)
    end = datetime.datetime.strptime(endStr,'%Y-%m-%d').replace(tzinfo=timezone.utc)

    selectedFields = ["Issue.key as issue", "Issue.storyPoints", "IssueType.name as issueType","Status.name as status","Issue.statusid", "Issue.assigneeName", "Issue.created", "Issue.updated"]
    joinClauses = [
        {"type":"LEFT", "tableName":"IssueType", "onClause":"Issue.issueTypeId = IssueType.id"},
        {"type":"LEFT", "tableName":"Project", "onClause":"Issue.projectId = Project.id"},
        {"type":"LEFT", "tableName":"Status", "onClause":"Issue.statusId = Status.id"}
    ]
    whereClause = "Project.key = '{}'".format(projectKey)
    statement = dbConnector.queryFromJoinStatement(selectedFields,"Issue",joinClauses,whereClause)

    # load data
    df = pd.read_sql_query(statement, dbConnector.connection)
    
    
    df["created"] = pd.to_datetime(df["created"])
    df["updated"] = pd.to_datetime(df["updated"])
    
    df_created = df[ (df["created"] >= start) & (df["created"]<=end) ]
    print("issue created between those days")
    print("count")
    print(df_created.groupby("status").count())
    print("story points")
    df_created = df_created.drop(df_created[df_created.storyPoints == "None"].index)
    df_created["storyPoints"] = pd.to_numeric(df_created["storyPoints"])
    print(df_created.groupby("status").sum())

    df_updated = df[ (df["updated"] >= start) & (df["updated"]<=end) ]
    print("issue updated between those days")
    print("count")
    print(df_updated.groupby("status").count())
    print("story points")
    df_updated = df_updated.drop(df_updated[df_updated.storyPoints == "None"].index)
    df_updated["storyPoints"] = pd.to_numeric(df_updated["storyPoints"])
    print(df_updated.groupby("status").sum())
    

    

def getIssueTypeMetrics():
    dbConnector = SqliteConnector()
    projectKeys = dbConnector.queryTable(["key"], "Project", None)
    # print(projectKeys) # [('PJA',), ('SP',)], the result comes as array of tuple
    if projectKeys is not None:
        for projectKey in projectKeys:
            print("--------------------------------------")
            print("Project: " + projectKey[0])
            print(getMetricsPerProject(projectKey[0]))
            print("--------------------------------------")


def issuesInSprint(sprintId):
    dbConnector = SqliteConnector()
    selectedFields = ["Issue.key as issue", "Issue.storyPoints", "IssueType.name as issueType","Status.name as status","Issue.statusid", "Issue.assigneeName", "Issue.created", "Issue.updated"]
    joinClauses = [
        {"type":"LEFT", "tableName":"IssueType", "onClause":"Issue.issueTypeId = IssueType.id"},
        {"type":"LEFT", "tableName":"Project", "onClause":"Issue.projectId = Project.id"},
        {"type":"LEFT", "tableName":"Status", "onClause":"Issue.statusId = Status.id"},
        {"type":"LEFT", "tableName":"SprintIssueLink", "onClause":"Issue.id = SprintIssueLink.issueId"},
    ]
    whereClause = "SprintIssueLink.sprintId = '{}'".format(sprintId)
    statement = dbConnector.queryFromJoinStatement(selectedFields,"Issue",joinClauses,whereClause)

    # load data
    df = pd.read_sql_query(statement, dbConnector.connection)
    print(df)
    print(df.groupby("status").count())    
    df = df.drop(df[df.storyPoints == "None"].index)
    df["storyPoints"] = pd.to_numeric(df["storyPoints"])
    print(df.groupby("status").sum())
    