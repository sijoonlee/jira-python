import json
from config import config

url = config.get("apiAddress") + "/search"
method = "POST"
def payload(projectKey, issueType ,maxResults, startAt):
    return json.dumps({
        "expand": [
            "changelog"
        ],
        "jql": "project = {projectKey} AND issueType = {issueType} AND status = 'In Progress'".format(projectKey = projectKey, issueType = issueType),
        "maxResults": maxResults,
        "fieldsByKeys": False,
        "fields": ["*all"], 
        # "fields" : ["issuetype", "summary", "created", "updated", "priority", "assignee", "creator", "reporter", "status", "timespent"],
        "startAt": startAt
    })
