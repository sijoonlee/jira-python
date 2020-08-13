import json
from config import config
from jira.jiraEndpoints.getIssuesInSprintPagination import method, url
from jira.jiraRequests.requestToJira import requestToJira

def getIssuesInSprintPagination(boardId, sprintId, maxResults, startAt):
    auth = config["auth"]
    formattedUrl = url.format(boardId=boardId, sprintId=sprintId, maxResults=maxResults, startAt=startAt)
    response = requestToJira(method, formattedUrl, auth, None)
    return json.loads(response.text)

def getAllIssuesInSprint(boardId, sprintId):
    maxResults = 50
    
    startAt = 0
    issues = []
    data = getIssuesInSprintPagination(boardId, sprintId, maxResults,startAt)
    if data.get("issues", None) is not None:
        for issue in data["issues"]:
            issues.append(issue)
        total = data["total"]
        
        while startAt < total:
            startAt += maxResults
            data = getIssuesInSprintPagination(boardId, sprintId, maxResults,startAt)
            for issue in data["issues"]:
                issues.append(issue)
    return issues
