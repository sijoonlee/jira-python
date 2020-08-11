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

if __name__=="__main__":
    dbFile = './db/sqlite3/storage/db.sqlite'
    dbConnector = SqliteConnector(dbFile)
    dbConnector.connection

    # dbConnector.dropTable(issueType.model)
    # dbConnector.dropTable(user.model)
    # dbConnector.dropTable(priority.model)
    # dbConnector.dropTable(status.model)
    # dbConnector.dropTable(project.model)
    # dbConnector.dropTable(issue.model)
    # dbConnector.dropTable(sprint.model)
    # dbConnector.dropTable(sprintIssueLink.model)
    
    # dbConnector.createTable(user.model)
    # dbConnector.createTable(priority.model)
    # dbConnector.createTable(project.model)
    # dbConnector.createTable(status.model)
    # dbConnector.createTable(issueType.model)
    # dbConnector.createTable(issue.model)
    # dbConnector.createTable(sprint.model)
    # dbConnector.createTable(sprintIssueLink.model)


    # response = getAllUsers()
    # dbReadyData = processResponse(user.lookup, response)
    # dbConnector.insertRecords(user.model, dbReadyData)

    # response = getAllProjects()
    # dbReadyData = processResponse(project.lookup, response)
    # dbConnector.insertRecords(project.model, dbReadyData)

    # response = getPriorities()
    # dbReadyData = processResponse(priority.lookup, response)
    # dbConnector.insertRecords(priority.model, dbReadyData)

    # response = getStatuses()
    # dbReadyData = processResponse(status.lookup, response)
    # dbConnector.insertRecords(status.model, dbReadyData)
    
    # response = getIssueTypes()
    # dbReadyData = processResponse(issueType.lookup, response)
    # dbConnector.insertRecords(issueType.model, dbReadyData)

    # response = getAllIssues()
    # dbReadyData = processResponse(issue.lookup, response)
    # dbConnector.insertRecords(issue.model, dbReadyData)

    # sprintRecordList, sprintIssueLinkRecordList = processSprint(response)
    # dbConnector.insertRecords(sprint.model, sprintRecordList)
    # dbConnector.insertRecords(sprintIssueLink.model, sprintIssueLinkRecordList)

    #
    selectedFields = ["Project.key as projectKey", "Issue.key as issueKey", "Issue.reporterName", "Status.name as status"]
    joinClauses = [
        {"type":"LEFT", "tableName":"IssueType", "onClause":"Issue.issueTypeId = IssueType.id"},
        {"type":"LEFT", "tableName":"Project", "onClause":"Issue.projectId = Project.id"},
        {"type":"LEFT", "tableName":"Status", "onClause":"Issue.statusId = Status.id"},
        {"type":"LEFT", "tableName":"Priority", "onClause":"Issue.priorityId = Priority.id"}
    ]
    statement = dbConnector.queryFromJoinStatement(selectedFields, "Issue", joinClauses, None)
    df = pd.read_sql_query(statement, dbConnector.connection)
    print(df)

    print("--------------------------------------")

    # join tables into one and dump the data into pandas
    selectedFields = ["Issue.key as issueKey", "IssueType.name as issueType"]
    joinClauses = [
        {"type":"LEFT", "tableName":"IssueType", "onClause":"Issue.issueTypeId = IssueType.id"},
        {"type":"LEFT", "tableName":"Status", "onClause":"Issue.statusId = Status.id"}
    ]
    statement = dbConnector.queryFromJoinStatement(selectedFields, "Issue", joinClauses, None)
    df = pd.read_sql_query(statement, dbConnector.connection)
    print(df)
    grouped = df.groupby('issueType').count()
    grouped['percentage'] = grouped['issueKey']/grouped['issueKey'].sum()
    print(grouped)
    