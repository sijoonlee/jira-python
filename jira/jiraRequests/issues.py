import json
from config import config
from jira.jiraEndpoints.getIssuesPagination import method, url, payloadGenerator
from jira.jiraRequests.requestToJira import requestToJira
import time
import concurrent.futures
from functools import partial

# https://support.atlassian.com/jira-software-cloud/docs/advanced-search-reference-jql-fields/
def getIssuesPagination(jqlQuery, maxResults, startAt):
    formattedUrl = url.format(maxResults=maxResults, startAt=startAt)
    auth = config["auth"]
    payloads = payloadGenerator(jqlQuery, maxResults, startAt)
    response = requestToJira(method, formattedUrl, auth, payloads)
    return json.loads(response.text)

def getIssues(jqlQuery = None): # no filtering to get all issues
    maxResults = 50
    startAt = 0
    issues = []
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
    
def getIssuesMultiThread(maxWorkers, jqlQuery=None):
    maxResults = 50
    startAt = 0
    issues = []
    data = getIssuesPagination(jqlQuery, maxResults, startAt)
    for issue in data["issues"]:
        issues.append(issue)
    total = data["total"]
    
    offsets = []
    partialGetIssuesPagination = partial(getIssuesPagination, jqlQuery, maxResults)
    while startAt < total:
        startAt += maxResults
        offsets.append(startAt)

    with concurrent.futures.ThreadPoolExecutor(max_workers=maxWorkers) as executor: #ProcessPoolExecutor(max_workers=2)
        # Start the load operations and mark each future with its URL
        for data in executor.map(partialGetIssuesPagination, offsets):
            for issue in data["issues"]:
                issues.append(issue)
    return issues

def getAllIssuesUpdatedAfter(updated):
    jqlQuery = "updated >= {}".format(updated)
    return getIssues(jqlQuery)

def getIssuesNotInSprint():
    return getIssues("sprint IS NULL")

def getIssuesNotInAnySprintWithUpdatedAfter(maxWorkers, updated):
    jqlQuery = "sprint IS EMPTY"
    if updated is not None:
        jqlQuery += " AND updated >= {}".format(updated)
    return getIssuesMultiThread(maxWorkers, jqlQuery)

def getIssuesInSprintWithUpdatedAfter(sprintId, updated=None):
    jqlQuery = "sprint = {}".format(sprintId)
    if updated is not None:
        jqlQuery += " AND updated >= {}".format(updated)
    return getIssues(jqlQuery)
