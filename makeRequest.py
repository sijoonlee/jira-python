import requests
from requests.auth import HTTPBasicAuth
import json
from config import config
import payloads.getProjectPagination
import payloads.getIssuesPagination



def getIssuesPagination(projectKey, maxResults, startAt):
    method = payloads.getIssuesPagination.method
    url = payloads.getIssuesPagination.url.format(domain = config['domain'])
    auth = HTTPBasicAuth(config['emailAccount'], config['apiToken'])
    payload = payloads.getIssuesPagination.payload(projectKey, maxResults, startAt)
    response = requestToJira(method, url, auth, payload)
    writeFileReport(response)


def getProjectPagination(maxResults, startAt):
    method = payloads.getProjectPagination.method
    url = payloads.getProjectPagination.url.format(domain = config['domain'], maxResults=maxResults, startAt=startAt)
    auth = HTTPBasicAuth(config['emailAccount'], config['apiToken'])
    response = requestToJira(method, url, auth, None)
    writeFileReport(response)


def requestToJira(method, url, auth, payload):
    headersDict = { 
        "GET" : { "Accept": "application/json","X-Atlassian-Token": 'no-check' },
        "POST" : {"Accept": "application/json", "Content-Type": "application/json", "X-Atlassian-Token": 'no-check'}
    }
    response = None
    if payload is None:
        response = requests.request(
            method,
            url,
            headers=headersDict[method],
            auth=auth
        )
    else :
        response = requests.request(
            method,
            url,
            headers=headersDict[method],
            data=payload,
            auth=auth
        )
    return response

def printResponseJson(response):
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

def writeFileReport(response):
    with open('response.json', 'w') as file:
        file.write(json.dumps(json.loads(response.text), indent=2))


if __name__=="__main__":
    # getProjectPagination(10,0)
    getIssuesPagination('PJA', 5, 0)