import json
from requests.auth import HTTPBasicAuth
from config import config
from jira.jiraEndpoints.getProjectPagination import method, url
from jira.jiraRequests.requestToJira import requestToJira

def getProjectPagination(maxResults, startAt):
    formattedUrl = url.format(maxResults=maxResults, startAt=startAt)
    auth = config["auth"]
    response = requestToJira(method, formattedUrl, auth, None)
    return json.loads(response.text)

def getAllProjects():
    maxResults = 50
    
    startAt = 0
    values = []
    data = getProjectPagination(maxResults,startAt)

    for value in data["values"]:
        values.append(value)
    total = data["total"]
    
    while startAt < total:
        startAt += maxResults
        data = getProjectPagination(maxResults,startAt)
        for value in data["values"]:
            values.append(value)
        if data["isLast"] is True:
            break
    
    return values
    