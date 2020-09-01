from businessLogic.metrics.metricsFunctions import countByGroup, percentageByGroup
from db.sqlite3.connector import SqliteConnector
from config import config

def getMetricsPerProject(projectKey):
    dbConnector = SqliteConnector()
    selectedFields = ["IssueType.name as issueType"]
    joinClauses = [
        {"type":"LEFT", "tableName":"IssueType", "onClause":"Issue.issueTypeId = IssueType.id"},
        {"type":"LEFT", "tableName":"Project", "onClause":"Issue.projectId = Project.id"}
    ]
    whereClause = "Project.key = '{}'".format(projectKey)
    statement = dbConnector.queryFromJoinStatement(selectedFields, "Issue", joinClauses, whereClause)
    df = percentageByGroup(dbConnector.connection, statement, "issueType")
    return df


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
    