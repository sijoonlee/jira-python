import json
from requests.auth import HTTPBasicAuth
from config import config
from jira.jiraEndpoints.getIssueTypes import method, url
from jira.jiraRequests.requestToJira import requestToJira

def getIssueTypes():
    auth = config["auth"]
    response = requestToJira(method, url, auth, None)
    return json.loads(response.text)