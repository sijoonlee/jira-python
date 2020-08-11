import json
from requests.auth import HTTPBasicAuth
from config import config
from jira.jiraEndpoints.getStatuses import method, url
from jira.jiraRequests.requestToJira import requestToJira

def getStatuses():
    auth = HTTPBasicAuth(config['emailAccount'], config['apiToken'])
    response = requestToJira(method, url, auth, None)
    return json.loads(response.text)