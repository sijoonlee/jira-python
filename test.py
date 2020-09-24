import re
from datetime import date
from db.postgres.connector import PostgresConnector
from db.redshift.connector import RedshiftConnector
from jira.jiraRequests.responseProcessor import responseProcessor
from businessLogic.db.dbActions import DbActions
from utils.jsonUtil import writeFileReport, readFileReport
import time
from table.user import User
from table.sprintIssueLink import SprintIssueLink
from jira.jiraRequests.users import getAllUsers
from utils.jsonUtil import readFileReport

# this is to fetch those data created/updated after a certain date
if __name__=="__main__":
    # use database connector you want to use - PostgresConnector, SqliteConnector, RedshiftConnector
    connector = PostgresConnector()
    record = {'id': '11771', 'key': 'CCOLD-75', 'summary': 'limit max width of top nav', 'storyPoints': 1.5, 'created': '2014-10-10T11:43:17.042-0400', 'updated': '2019-05-06T08:33:17.978-0400', 'resolutionId': '1', 'resolutionDate': '2014-11-06T12:12:15.818-0500', 'parentId': None, 'parentKey': None, 'parentSummary': None, 'issueTypeId': '3', 'priorityId': '3', 'statusId': '10100', 'projectId': '10014', 'creatorId': '557058:cd6fb800-d308-4785-b2f2-133512282041', 'reporterId': '557058:cd6fb800-d308-4785-b2f2-133512282041', 'assigneeId': '557058:cd6fb800-d308-4785-b2f2-133512282041', 'leadDevId': '557058:49bf5c91-2deb-4209-8733-504d8b0ad6c0', 'leadQAId': None, 'creatorName': 'Kurtis Elliott [Administrator]', 'reporterName': 'Kurtis Elliott [Administrator]', 'assigneeName': 'Kurtis Elliott [Administrator]', 'leadDevName': 'Brandon Legault', 'leadQAName': None}
    #print(connector.insertValuesStatement(issue.model, record))

    # User.drop(connector)
    # User.create(connector)

    # responseUser = getAllUsers()
    # User.update(connector, responseProcessor, responseUser)
    model = {
        "name" : "SprintIssueLink",
        "fields" : [
            {"name" : "sprintId", "type" : "TEXT" },
            {"name" : "issueId", "type" : "TEXT" }
        ],
        "primaryKeys" : [ "sprintId", "issueId" ]#,
        # "foreignKeys" : [
        #     {"name": "sprintId", "references": "Sprint(id)"},
        #     {"name": "issueId", "references": "Issue(id)"},
        # ]
    }
    resp = {
        "sprintId": 514,
        "issueId": "37644"
    }
    
    print(connector.insertValuesStatement(model,resp))

    res = readFileReport('res.json')
    col = readFileReport('coll.json')

    
    resIds = (item['id']  for item in res)
    colIds = (item['id'] for item in col)

    resSet = set(resIds)
    colSet = set(colIds)
    
    print(len(resSet))
    un = resSet.union(colSet)
    print(len(un))
    
