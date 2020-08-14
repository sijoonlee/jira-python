import json
from config import config
from jira.jiraEndpoints.getBoardPagination import method, url
from jira.jiraRequests.requestToJira import requestToJira

def getBoardPagination(maxResults, startAt):
    auth = config["auth"]
    formattedUrl = url.format(maxResults=maxResults, startAt=startAt)
    response = requestToJira(method, formattedUrl, auth, None)
    return json.loads(response.text)

def getAllBoards():
    maxResults = 50
    
    startAt = 0
    values = []
    data = getBoardPagination(maxResults,startAt)

    for value in data["values"]:
        values.append(value)
    total = data["total"]
    
    while startAt < total:
        startAt += maxResults
        data = getBoardPagination(maxResults,startAt)
        for value in data["values"]:
            values.append(value)
        if data["isLast"] is True:
            break
    
    return values