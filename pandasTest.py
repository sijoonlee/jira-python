import pandas as pd
from db.sqlite3.connector import SqliteConnector
from model import issue, priority, project, status, issueType, user, sprint, sprintIssueLink
from jiraRequests.issues import getAllIssues
from jiraRequests.issueTypes import getIssueTypes
from jiraRequests.priorities import getPriorities
from jiraRequests.projects import getAllProjects
from jiraRequests.statuses import getStatuses
from jiraRequests.users import getAllUsers
from jiraRequests.processResponse import processResponse
from jiraRequests.processSprint import processSprint
from businessLogic.metrics.issueType import getIssueTypeMetrics
import businessLogic.db.dbActions as dbActions

if __name__=="__main__":
    dbFile = './db/sqlite3/storage/db.sqlite'
    dbConnector = SqliteConnector(dbFile)
    dbActions.reset(dbConnector)
    dbActions.update(dbConnector)

    selectedFields = ["Project.key as projectKey", "Issue.key as issueKey", "Issue.reporterName", "Status.name as status"]
    joinClauses = [
        {"type":"LEFT", "tableName":"IssueType", "onClause":"Issue.issueTypeId = IssueType.id"},
        {"type":"LEFT", "tableName":"Project", "onClause":"Issue.projectId = Project.id"},
        {"type":"LEFT", "tableName":"Status", "onClause":"Issue.statusId = Status.id"},
        {"type":"LEFT", "tableName":"Priority", "onClause":"Issue.priorityId = Priority.id"}
    ]
    whereClause = "Project.key = 'PJA'"
    statement = dbConnector.queryFromJoinStatement(selectedFields, "Issue", joinClauses, whereClause)
    df = pd.read_sql_query(statement, dbConnector.connection)
    print(df)

    print("--------------------------------------")

    getIssueTypeMetrics()