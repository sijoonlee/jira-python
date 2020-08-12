import pandas as pd
from db.sqlite3.connector import SqliteConnector
from model import issue, priority, project, status, issueType, user, sprint, sprintIssueLink
from jira.jiraRequests.issues import getAllIssues
from jira.jiraRequests.issueTypes import getIssueTypes
from jira.jiraRequests.priorities import getPriorities
from jira.jiraRequests.projects import getAllProjects
from jira.jiraRequests.statuses import getStatuses
from jira.jiraRequests.users import getAllUsers
from jira.jiraRequests.processResponse import processResponse
from jira.jiraRequests.processSprint import processSprint
from businessLogic.metrics.issueType import getIssueTypeMetrics
import businessLogic.db.dbActions as dbActions

if __name__=="__main__":
    dbFile = './db/sqlite3/storage/db.sqlite'
    dbConnector = SqliteConnector(dbFile)
    dbActions.reset(dbConnector)
    dbActions.update(dbConnector)

    print("--------------------------------------")

    # Finding Issues not beloning to any Sprint
    selectedFields = ["Issue.key as issueKey", "IssueType.name as issueType","Sprint.id as sprintId", "Sprint.name as sprintName"]
    joinClauses = [
        {"type":"LEFT", "tableName":"IssueType", "onClause":"Issue.issueTypeId = IssueType.id"},
        {"type":"LEFT", "tableName":"SprintIssueLink", "onClause":"Issue.id = SprintIssueLink.issueId"},
        {"type":"LEFT", "tableName":"Sprint", "onClause":"Sprint.id = SprintIssueLink.sprintId"},
    ]
    whereClause = "Sprint.id IS NULL"
    statement = dbConnector.queryFromJoinStatement(selectedFields, "Issue", joinClauses, whereClause)
    df = pd.read_sql_query(statement, dbConnector.connection)
    print(df)

    print("--------------------------------------")
    # Project PJA's general info
    selectedFields = ["Project.key as projectKey", "Issue.key as issueKey", "Issue.reporterName", "Status.name as status", "Priority.name as priority"]
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

    # IssueTypes information
    getIssueTypeMetrics()