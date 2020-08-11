import requests

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