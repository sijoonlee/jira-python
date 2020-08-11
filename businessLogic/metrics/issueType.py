from businessLogic.metrics.metricsFunctions import countByGroup, percentageByGroup
from db.sqlite3.connector import SqliteConnector

dbFile = './db/sqlite3/storage/db.sqlite'
dbConnector = SqliteConnector(dbFile)

def getMetricsPerProject(projectKey):
    selectedFields = ["Project.key as projectKey", "IssueType.name as issueType", "Status.name as status", "Priority.name as priority"]
    joinClauses = [
        {"type":"LEFT", "tableName":"IssueType", "onClause":"Issue.issueTypeId = IssueType.id"},
        {"type":"LEFT", "tableName":"Project", "onClause":"Issue.projectId = Project.id"},
        {"type":"LEFT", "tableName":"Status", "onClause":"Issue.statusId = Status.id"},
        {"type":"LEFT", "tableName":"Priority", "onClause":"Issue.priorityId = Priority.id"}
    ]
    whereClause = "Project.key = '{}'".format(projectKey)
    statement = dbConnector.queryFromJoinStatement(selectedFields, "Issue", joinClauses, whereClause)
    df = percentageByGroup(dbConnector.connection, statement, "issueType")
    return df


def getIssueTypeMetrics():
    projectKeys = dbConnector.queryTable("Project", ["key"], None)
    # print(projectKeys) # [('PJA',), ('SP',)], the result comes as array of tuple
    if projectKeys is not None:
        for projectKey in projectKeys:
            print("Project: " + projectKey[0])
            print(getMetricsPerProject(projectKey[0]))
    