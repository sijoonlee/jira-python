import json
from config import cloudApiAddress
DEFAULT_FIELDS = [ "issuetype", "summary", "priority", "status", "project", "parent", "fixVersions",
                "resolution", "resolutiondate",
                "customfield_10004","customfield_10006","customfield_10820","customfield_10821",
                "created", "updated", # "timespent",
                "assignee", "creator", "reporter"] # ["*all"] # to get all fields
DEFAULT_EXPAND = [] # ["changelog"] # unnecessary for now

#customfield_10004: story point
#customfield_10006: sprint
#customfield_10820: user, lead dev
#customfield_10821: user, lead qa

url = cloudApiAddress + "/search"
method = "POST"

class PayloadsBuilder(object):
    def __init__(self):
        self.payload = {}
        self.defaultSetting()

    def defaultSetting(self):
        self.payload["fieldsByKeys"] = False

    def withExpand(self, *args):
        if len(args) > 0:
            self.payload["expand"] = []
            for arg in args:
                self.payload["expand"].append(arg)
        return self

    def withJQL(self, query):
        if query is not None:
            self.payload["jql"] = query
        return self

    def withFields(self, *args):
        self.payload["fields"] = []
        for arg in args:
            self.payload["fields"].append(arg)
        return self

    def withPagination(self, maxResults, startAt):
        self.payload["maxResults"] = maxResults
        self.payload["startAt"] = startAt
        return self
    
    def getPayloads(self):
        return json.dumps(self.payload)


def payloadGenerator(jqlQuery, maxResults, startAt):
    builder = PayloadsBuilder()
    payloads = builder\
        .withExpand(*DEFAULT_EXPAND)\
        .withFields(*DEFAULT_FIELDS)\
        .withJQL(jqlQuery)\
        .withPagination(maxResults, startAt)\
        .getPayloads()
    
    return payloads