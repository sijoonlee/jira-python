# import os
from db.sqlite3.connector import SqliteConnector
from model import issue, priority, project, status, issueType, user, sprint, sprintIssueLink
    

if __name__=="__main__":
    
    # path = os.path.dirname(os.path.abspath(__file__))
    dbFile = './db/sqlite3/storage/db.sqlite'
    dbConnector = SqliteConnector(dbFile)

    
    dbConnector.dropTable(issueType.model)
    dbConnector.dropTable(user.model)
    dbConnector.dropTable(priority.model)
    dbConnector.dropTable(status.model)
    dbConnector.dropTable(project.model)
    dbConnector.dropTable(issue.model)
    dbConnector.dropTable(sprint.model)
    dbConnector.dropTable(sprintIssueLink.model)

    dbConnector.createTable(user.model)
    dbConnector.createTable(priority.model)
    dbConnector.createTable(project.model)
    dbConnector.createTable(status.model)
    dbConnector.createTable(issueType.model)
    dbConnector.createTable(issue.model)
    dbConnector.createTable(sprint.model)
    dbConnector.createTable(sprintIssueLink.model)


    userData = [
        {
            "accountId" : "USER_ID_1",
            "accountType" : "atlassian",
            "emailAddress" : "USER_EMAIL_1",
            "displayName" : "USER_NAME_1",
            "active" : 1
        },
        {
            "accountId" : "USER_ID_2",
            "accountType" : "atlassian",
            "emailAddress" : "USER_EMAIL_2",
            "displayName" : "USER_NAME_2",
            "active" : 1
        }
    ]

    dbConnector.insertRecords(user.model, userData)


    priorityData = [
        { "id":"1", "name":"Important", "description":"really important"},
        { "id":"2", "name":"Normal", "description":"normal level"},
        { "id":"3", "name":"Not urgent", "description":"not really important"}
    ]

    dbConnector.insertRecords(priority.model, priorityData)


    projectData = [
        {"id":"1", "key":"PJ-1", "name":"project 1", "style":"classic"},
        {"id":"2", "key":"PJ-2", "name":"project 2", "style":"classic"},
        {"id":"3", "key":"PJ-3", "name":"project 3", "style":"classic"}
    ]

    dbConnector.insertRecords(project.model, projectData)

    statusData = [
        {"id":"1", "name":"Done", "description":"Task is done", "projectId":"1"},
        {"id":"2", "name":"In Progress", "description":"Task is in process", "projectId":"1"},
        {"id":"3", "name":"Done", "description":"Task is done", "projectId":"2"},
        {"id":"4", "name":"TODO", "description":"Task is in process", "projectId":"2"}
    ]

    dbConnector.insertRecords(status.model, statusData)

    issueTypeData = [
        {"id":"1", "name":"Epic", "projectId":"1"},
        {"id":"2", "name":"Story", "projectId":"1"},
        {"id":"3", "name":"Task", "projectId":"1"},
        {"id":"4", "name":"Epic", "projectId":"2"},
        {"id":"5", "name":"Crazy", "projectId":None}
    ]

    dbConnector.insertRecords(issueType.model, issueTypeData)

    issueData = [
        {
            "id":"1000", "key":"FirstIssue", "summary":"this is the first issue", 
            "created":"2020-08-06T11:44:57.334-0400", "updated":"2020-08-07T11:44:57.334-0400",
            "parentId":"1001", "parentKey":"SecondIssue", "parentSummary":"this is the second issue",
            "issueTypeId":"1", "priorityId":"1", "statusId":"2", "projectId":"1", 
            "creatorId":"USER_ID_1", "reporterId":"USER_ID_1", "assigneeId":"USER_ID_2",
            "creatorName":"USER_NAME_1", "reporterName":"USER_NAME_1", "assigneeName":"USER_NAME_2"
        },
        {
            "id":"1001", "key":"SecondIssue", "summary":"this is the second issue", 
            "created":"2020-08-06T11:44:57.334-0400", "updated":"2020-08-07T11:44:57.334-0400",
            "issueTypeId":"2", "priorityId":"1", "statusId":"1", "projectId":"1", 
            "creatorId":"USER_ID_1", "reporterId":"USER_ID_1", "assigneeId":"USER_ID_2",
            "creatorName":"USER_NAME_1", "reporterName":"USER_NAME_1", "assigneeName":"USER_NAME_2"
        },
        {
            "id":"1002", "key":"FirstIssue", "summary":"this is the first issue", 
            "created":"2020-08-06T11:44:57.334-0400", "updated":"2020-08-07T11:44:57.334-0400",
            "issueTypeId":"1", "priorityId":"1", "statusId":"1", "projectId":"2", 
            "creatorId":"USER_ID_1", "reporterId":"USER_ID_1", "assigneeId":"USER_ID_2",
            "creatorName":"USER_NAME_1", "reporterName":"USER_NAME_1", "assigneeName":"USER_NAME_2"
        }
    ]

    dbConnector.insertRecords(issue.model, issueData)

    sprintData = [
        {
            'id': '1', 'name': 'SP Sprint 1', 'goal': None, 'state': 'CLOSED', 
            'startDate': '2020-08-057T19:07:29.401Z', 
            'endDate': '2020-08-29T19:07:22.000Z', 
            'completeDate': '2020-08-12T13:40:59.447Z'
        },
        {
            'id': '2', 'name': 'SP Sprint 2', 'goal': "testing", 'state': 'CLOSED', 
            'startDate': '2020-08-07T19:07:29.401Z', 
            'endDate': '2020-08-28T19:07:22.000Z', 
            'completeDate': '2020-08-11T13:40:59.447Z'
        }
    ]
    dbConnector.insertRecords(sprint.model, sprintData)

    sprintIssueLinkData = [
        {
            'sprintId': '1',
            'issueId': '1000'
        },
        {
            'sprintId': '2',
            'issueId': '1000'
        },
        {
            'sprintId': '1',
            'issueId': '1001'
        }
    ]
    dbConnector.insertRecords(sprintIssueLink.model, sprintIssueLinkData)


    selectedFields = ["Issue.id", "Issue.key", "Issue.projectId"]
    whereClause = 'projectId = "1" AND issueTypeId = "2"'
    result = dbConnector.queryTable("Issue", selectedFields, whereClause)
    print(result)

    selectedFields = ["Project.key", "Issue.key", "Issue.reporterName", "Status.name"]
    joinClauses = [
        {"type":"LEFT", "tableName":"IssueType", "onClause":"Issue.issueTypeId = IssueType.id"},
        {"type":"LEFT", "tableName":"Project", "onClause":"Issue.projectId = Project.id"},
        {"type":"LEFT", "tableName":"Status", "onClause":"Issue.statusId = Status.id"},
        {"type":"LEFT", "tableName":"Priority", "onClause":"Issue.priorityId = Priority.id"}
    ]
    whereClause = 'Issue.projectId = "1"'
    result = dbConnector.queryFromJoin(selectedFields, "Issue", joinClauses, whereClause)
    print(result)
    
    selectedFields = ["Project.key", "Issue.key", "Issue.reporterName", "Status.name"]
    joinClauses = [
        {"type":"LEFT", "tableName":"IssueType", "onClause":"Issue.issueTypeId = IssueType.id"},
        {"type":"LEFT", "tableName":"Project", "onClause":"Issue.projectId = Project.id"},
        {"type":"LEFT", "tableName":"Status", "onClause":"Issue.statusId = Status.id"},
        {"type":"LEFT", "tableName":"Priority", "onClause":"Issue.priorityId = Priority.id"}
    ]
    whereClause = 'Issue.projectId = "1"'
    result = dbConnector.queryFromJoin(selectedFields, "Issue", joinClauses, whereClause)
    print(result)