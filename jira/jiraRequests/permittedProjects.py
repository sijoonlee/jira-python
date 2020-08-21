import json
from requests.auth import HTTPBasicAuth
from config import config
from jira.jiraEndpoints.getPermittedProjects import method, url
from jira.jiraRequests.requestToJira import requestToJira

def getPermittedProjects():
    auth = config["auth"]
    query =  json.dumps({'permissions': ["BROWSE_PROJECTS", "EDIT_ISSUES"]}) #["<string>"]}
    response = requestToJira(method, url, auth, query)
    return json.loads(response.text)