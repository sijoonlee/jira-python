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
    elif method == "POST":
        response = requests.request(
            method,
            url,
            headers=headersDict[method],
            data=payload,
            auth=auth
        )
    elif method == "GET":
        response = requests.request(
            method,
            url,
            headers=headersDict[method],
            params=payload,
            auth=auth
        )
    else:
        print("Method should be GET or POST")
    return response