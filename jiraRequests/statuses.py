import json
from requests.auth import HTTPBasicAuth
from config import config
from jiraEndpoints.getStatuses import method, url
from jiraRequests.requestToJira import requestToJira

def getStatuses():
    auth = HTTPBasicAuth(config['emailAccount'], config['apiToken'])
    response = requestToJira(method, url, auth, None)
    return json.loads(response.text)