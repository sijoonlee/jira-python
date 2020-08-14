import json
from requests.auth import HTTPBasicAuth
from config import config
from jira.jiraEndpoints.getResolution import method, url
from jira.jiraRequests.requestToJira import requestToJira


def getResolutions():
    auth = config["auth"]
    response = requestToJira(method, url, auth, None)
    return json.loads(response.text)