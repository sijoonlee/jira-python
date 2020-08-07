import json

url = "https://{domain}.atlassian.net/rest/api/3/search"
method = "POST"
def payload(projectKey, maxResults, startAt):
    return json.dumps({
        "expand": [
            "changelog"
        ],
        "jql": "project = {projectKey} AND issueType = Story".format(projectKey = projectKey),
        "maxResults": maxResults,
        "fieldsByKeys": False,
        "fields": ["*all"], 
        # "fields" : ["created", "updated", "priority", "assignee", "creator", "reporter", "status"],
        "startAt": startAt
    })
