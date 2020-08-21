import json
from requests.auth import HTTPBasicAuth
from config import config
from jira.jiraEndpoints.getMyPermission import method, url
from jira.jiraRequests.requestToJira import requestToJira

def getMyPermission():
    auth = config["auth"]
    query = {'permissions': 'BROWSE_PROJECTS,EDIT_ISSUES'}
    response = requestToJira(method, url, auth, query)
    return json.loads(response.text)