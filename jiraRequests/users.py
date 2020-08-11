import json
from requests.auth import HTTPBasicAuth
from config import config
from jiraEndpoints.getUsers import method, url
from jiraRequests.requestToJira import requestToJira

def getAllUsers():
    auth = HTTPBasicAuth(config['emailAccount'], config['apiToken'])
    response = requestToJira(method, url, auth, None)
    return json.loads(response.text)