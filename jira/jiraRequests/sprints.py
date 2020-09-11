import json
import sys
from requests.auth import HTTPBasicAuth
from config import config
from jira.jiraEndpoints.getSprintsInBoardPagination import method, url
from jira.jiraRequests.requestToJira import requestToJira

def getSprintsInBoardPagination(boardId, maxResults, startAt):
    auth = config["auth"]
    formattedUrl = url.format(boardId=boardId, maxResults=maxResults, startAt=startAt)
    result = None
    response = None
    try:
        response = requestToJira(method, formattedUrl, auth, None)
        result = json.loads(response.text)
    except:
        print(sys.exc_info())
        print("Error in getSprintsInBoardPagination")
        print("Board id:", boardId)
        print("Start At:", startAt)
        print("Response:", response.text)
    return result


def getAllSprintsInBoard(boardId):
    maxResults = 50 # don't change this value, jira API only supports 50 for now
    
    startAt = 0
    values = []
    data = getSprintsInBoardPagination(boardId, maxResults,startAt)
    if data.get("values", None) is not None:
        for value in data["values"]:
            values.append(value)
        
        while data["isLast"] is False:
            startAt += maxResults
            data = getSprintsInBoardPagination(boardId, maxResults,startAt)
            for value in data["values"]:
                values.append(value)
            if data["isLast"] is True:
                break
    
    return values