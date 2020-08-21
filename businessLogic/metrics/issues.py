from businessLogic.metrics.metricsFunctions import countByGroup, percentageByGroup
from db.sqlite3.connector import SqliteConnector

def issueCountPerProject():
    dbFile = './db/sqlite3/storage/db.sqlite'
    dbConnector = SqliteConnector(dbFile)
    selectedFields = ["Project.name as project"]
    joinClauses = [
        {"type":"LEFT", "tableName":"Project", "onClause":"Issue.projectId = Project.id"}
    ]
    statement = dbConnector.queryFromJoinStatement(selectedFields, "Issue", joinClauses, None)
    df = countByGroup(dbConnector.connection,statement,"project")
    return df
