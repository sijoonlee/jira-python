import json
from requests.auth import HTTPBasicAuth
from config import config
from jira.jiraEndpoints.getUsers import method, url
from jira.jiraRequests.requestToJira import requestToJira

def getAllUsers():
    auth = HTTPBasicAuth(config['emailAccount'], config['apiToken'])
    response = requestToJira(method, url, auth, None)
    return json.loads(response.text)