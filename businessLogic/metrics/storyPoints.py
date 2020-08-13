from businessLogic.metrics.metricsFunctions import countByGroup, percentageByGroup
from db.sqlite3.connector import SqliteConnector
import pandas as pd
import datetime
from datetime import timezone
dbFile = './db/sqlite3/storage/db.sqlite'
dbConnector = SqliteConnector(dbFile)

def getMetricsPerProject(projectKey):
    selectedFields = ["Issue.key as issue", "Issue.storyPoints", "IssueType.name as issueType","Status.name as status", "Issue.assigneeName", "Issue.created"]
    joinClauses = [
        {"type":"LEFT", "tableName":"IssueType", "onClause":"Issue.issueTypeId = IssueType.id"},
        {"type":"LEFT", "tableName":"Project", "onClause":"Issue.projectId = Project.id"},
        {"type":"LEFT", "tableName":"Status", "onClause":"Issue.statusId = Status.id"}
    ]
    whereClause = "Project.key = '{}'".format(projectKey)
    statement = dbConnector.queryFromJoinStatement(selectedFields,"Issue",joinClauses,whereClause)

    # df = percentageByGroup(dbConnector.connection, statement, "issueType")
    df = pd.read_sql_query(statement, dbConnector.connection)

    # parse string to datetime
    df["created"] = pd.to_datetime(df["created"])

    # filter > 2020.1.1
    df = df[df["created"] > datetime.datetime(year=2020,month=1,day=1).replace(tzinfo=timezone.utc)]
    
    # drop data where story points are none
    df = df.drop(df[df.storyPoints == "None"].index)
    df["storyPoints"] = pd.to_numeric(df["storyPoints"])


    df1 = df.groupby("assigneeName").sum()
    print(df1)
    df2 = df.groupby("issueType").sum()
    print(df2)
    df = df.groupby("status").sum()
    
    #df = df.groupby("storyPoints").count()
    return df


def getIssueTypeMetrics():
    projectKeys = dbConnector.queryTable("Project", ["key"], None)
    # print(projectKeys) # [('PJA',), ('SP',)], the result comes as array of tuple
    if projectKeys is not None:
        for projectKey in projectKeys:
            print("--------------------------------------")
            print("Project: " + projectKey[0])
            print(getMetricsPerProject(projectKey[0]))
            print("--------------------------------------")