import pandas as pd
from db.sqlite3.connector import SqliteConnector
from table import issue, priority, project, status, issueType, user, sprint, sprintIssueLink
from jira.jiraRequests.issues import getAllIssues
from jira.jiraRequests.issueTypes import getIssueTypes
from jira.jiraRequests.priorities import getPriorities
from jira.jiraRequests.projects import getAllProjects
from jira.jiraRequests.statuses import getStatuses
from jira.jiraRequests.users import getAllUsers
from jira.jiraRequests.responseProcessor import responseProcessor
from businessLogic.db import dbActions

if __name__=="__main__":
    dbFile = './db/sqlite3/storage/db.sqlite'
    dbConnector = SqliteConnector(dbFile)

    selectedFields = ["Project.key", "Issue.key", "Issue.reporterName", "Status.name"]
    joinClauses = [
        {"type":"LEFT", "tableName":"IssueType", "onClause":"Issue.issueTypeId = IssueType.id"},
        {"type":"LEFT", "tableName":"Project", "onClause":"Issue.projectId = Project.id"},
        {"type":"LEFT", "tableName":"Status", "onClause":"Issue.statusId = Status.id"},
        {"type":"LEFT", "tableName":"Priority", "onClause":"Issue.priorityId = Priority.id"}
    ]
    whereClause = 'Issue.projectId = "11129"'
    result = dbConnector.queryFromJoin(selectedFields, "Issue", joinClauses, whereClause)
    print(result)


    selectedFields = ["Sprint.name", "Issue.summary", "IssueType.name"]
    joinClauses = [
        {"type":"LEFT", "tableName":"Issue", "onClause":"Issue.id = SprintIssueLink.issueId"},
        {"type":"LEFT", "tableName":"Sprint", "onClause":"Sprint.id = SprintIssueLink.sprintId"},
        {"type":"LEFT", "tableName":"IssueType", "onClause":"Issue.issueTypeId = IssueType.id"}
    ]
    whereClause = 'Issue.projectId = "11129"'
    result = dbConnector.queryFromJoin(selectedFields, "SprintIssueLink", joinClauses, whereClause)
    print(result)


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
    whereClause = "Project.key = 'OMP'"
    statement = dbConnector.queryFromJoinStatement(selectedFields, "Issue", joinClauses, whereClause)
    df = pd.read_sql_query(statement, dbConnector.connection)
    print(df)

    print("--------------------------------------")