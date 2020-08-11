import json
from requests.auth import HTTPBasicAuth
from config import config
from jira.jiraEndpoints.getIssuesPagination import method, url, payloadGenerator
from jira.jiraRequests.requestToJira import requestToJira

def getFilteredIssues(projectKey, issueType):
    maxResults = 50
    startAt = 0
    issues = []
    jqlQuery = {"project":projectKey, "issueType":issueType} # no filtering to get all issues
    data = getIssuesPagination(jqlQuery, maxResults, startAt)

    for issue in data["issues"]:
        issues.append(issue)
    total = data["total"]
    
    while startAt < total:
        startAt += maxResults
        data = getIssuesPagination({}, maxResults,startAt)
        for issue in data["issues"]:
            issues.append(issue)
    
    return issues    

def getIssuesPagination(jqlQuery, maxResults, startAt):
    formattedUrl = url.format(maxResults=maxResults, startAt=startAt)
    auth = HTTPBasicAuth(config['emailAccount'], config['apiToken'])
    payloads = payloadGenerator(jqlQuery, maxResults, startAt)
    response = requestToJira(method, formattedUrl, auth, payloads)
    return json.loads(response.text)

def getAllIssues():
    maxResults = 50
    startAt = 0
    issues = []
    jqlQuery = {} # no filtering to get all issues
    data = getIssuesPagination(jqlQuery, maxResults, startAt)

    for issue in data["issues"]:
        issues.append(issue)
    total = data["total"]
    
    while startAt < total:
        startAt += maxResults
        data = getIssuesPagination({}, maxResults,startAt)
        for issue in data["issues"]:
            issues.append(issue)
    
    return issues
    