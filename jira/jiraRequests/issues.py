import json
from config import config
from jira.jiraEndpoints.getIssuesPagination import method, url, payloadGenerator
from jira.jiraRequests.requestToJira import requestToJira

def getIssuesPagination(jqlQuery, maxResults, startAt):
    formattedUrl = url.format(maxResults=maxResults, startAt=startAt)
    auth = config["auth"]
    payloads = payloadGenerator(jqlQuery, maxResults, startAt)
    response = requestToJira(method, formattedUrl, auth, payloads)
    return json.loads(response.text)

def getAllIssuesUpdatedAfter(updated):
    maxResults = 50
    startAt = 0
    issues = []
    jqlQuery = "updated >= {}".format(updated)
    data = getIssuesPagination(jqlQuery, maxResults, startAt)

    for issue in data["issues"]:
        issues.append(issue)
    total = data["total"]
    
    while startAt < total:
        startAt += maxResults
        data = getIssuesPagination(jqlQuery, maxResults,startAt)
        for issue in data["issues"]:
            issues.append(issue)
    return issues    

# https://support.atlassian.com/jira-software-cloud/docs/advanced-search-reference-jql-fields/
def getIssuesNotInAnySprintWithUpdatedAfter(updated):
    maxResults = 50
    startAt = 0
    issues = []
    jqlQuery = "sprint IS EMPTY"
    if updated is not None:
        jqlQuery += " AND updated >= {}".format(updated)
    data = getIssuesPagination(jqlQuery, maxResults, startAt)
    for issue in data["issues"]:
        issues.append(issue)
    total = data["total"]
    
    while startAt < total:
        startAt += maxResults
        data = getIssuesPagination(jqlQuery, maxResults,startAt)
        for issue in data["issues"]:
            issues.append(issue)
    return issues

# https://support.atlassian.com/jira-software-cloud/docs/advanced-search-reference-jql-fields/
def getIssuesInSprintWithUpdatedAfter(sprintId, updated=None):
    maxResults = 50
    startAt = 0
    issues = []
    jqlQuery = "sprint = {}".format(sprintId)
    if updated is not None:
        jqlQuery += " AND updated >= {}".format(updated)
    data = getIssuesPagination(jqlQuery, maxResults, startAt)
    for issue in data["issues"]:
        issues.append(issue)
    total = data["total"]
    
    while startAt < total:
        startAt += maxResults
        data = getIssuesPagination(jqlQuery, maxResults,startAt)
        for issue in data["issues"]:
            issues.append(issue)
    return issues

def getIssuesNotInProject():
    maxResults = 50
    startAt = 0
    issues = []
    jqlQuery = "sprint IS NULL"
    data = getIssuesPagination(jqlQuery, maxResults, startAt)
    for issue in data["issues"]:
        issues.append(issue)
    total = data["total"]
    print(total)
    while startAt < total:
        startAt += maxResults
        data = getIssuesPagination(jqlQuery, maxResults,startAt)
        for issue in data["issues"]:
            issues.append(issue)
    return issues

def getAllIssues(jqlQuery = None): # no filtering to get all issues
    maxResults = 50
    startAt = 0
    issues = []
    data = getIssuesPagination(jqlQuery, maxResults, startAt)

    for issue in data["issues"]:
        issues.append(issue)
    total = data["total"]
    print(total)
    while startAt < total:
        startAt += maxResults
        data = getIssuesPagination(jqlQuery, maxResults,startAt)
        for issue in data["issues"]:
            issues.append(issue)
    
    return issues
    