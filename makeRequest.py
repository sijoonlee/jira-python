import collections
import requests
import json
from requests.auth import HTTPBasicAuth
from config import config
import payloads.getProjectPagination
import payloads.getIssuesPagination
import payloads.getIssueType
import payloads.getAnIssue
import payloads.getStatuses


def getIssueType():
    method = payloads.getIssueType.method
    url = payloads.getIssueType.url.format(domain = config['domain'])
    auth = HTTPBasicAuth(config['emailAccount'], config['apiToken'])
    response = requestToJira(method, url, auth, None)
    return json.loads(response.text)

def extractIssueNameID(issueTypesInJson):
    IssueTypeTuple = collections.namedtuple('IssueType', ['id', 'name'])
    issueTypes = []
    for issueType in issueTypesInJson:
        issueTypes.append(IssueTypeTuple(issueType["id"],issueType["name"]))
    return issueTypes
  

def getIssuesPagination(projectKey, issueType, maxResults, startAt):
    method = payloads.getIssuesPagination.method
    url = payloads.getIssuesPagination.url
    auth = HTTPBasicAuth(config['emailAccount'], config['apiToken'])
    payload = payloads.getIssuesPagination.payload(projectKey, issueType, maxResults, startAt)
    response = requestToJira(method, url, auth, payload)
    return json.loads(response.text)


def getProjectPagination(maxResults, startAt):
    method = payloads.getProjectPagination.method
    url = payloads.getProjectPagination.url.format(domain = config['domain'], maxResults=maxResults, startAt=startAt)
    auth = HTTPBasicAuth(config['emailAccount'], config['apiToken'])
    response = requestToJira(method, url, auth, None)
    return json.loads(response.text)


def getAnIssue(issueID):
    method = payloads.getAnIssue.method
    url = payloads.getAnIssue.url.format(domain = config['domain'], issue = issueID)
    auth = HTTPBasicAuth(config['emailAccount'], config['apiToken'])
    response = requestToJira(method, url, auth, None)
    return json.loads(response.text)

def getStatuses():
    method = payloads.getStatuses.method
    url = payloads.getStatuses.url.format(domain = config['domain'])
    auth = HTTPBasicAuth(config['emailAccount'], config['apiToken'])
    response = requestToJira(method, url, auth, None)
    return json.loads(response.text)



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

def printResponseJson(data):
    print(json.dumps(data, sort_keys=True, indent=4, separators=(",", ": ")))

def readFileReport(filename):
    data = None
    with open(filename) as file:
        data = json.load(file)
    return data

def writeFileReport(data):
    with open('response.json', 'w') as file:
        file.write(json.dumps(data, indent=2))


if __name__=="__main__":
    # getProjectPagination(10,0)

    # issueTypesAllData = getIssueType()
    # issueTypeNameID = extractIssueNameID(issueTypesAllData)

    # for issueType in issueTypeNameID:
    #     result = getIssuesPagination('PJA', issueType.id, 5, 0)
    #     print(issueType.id, issueType.name, result['total'])
    
    data = getIssuesPagination('PJA', 10000, 6, 0)
    # data  = getStatuses()
    # data = getAnIssue(10001)
    writeFileReport(data)

    