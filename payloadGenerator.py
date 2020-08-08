
import json

KEY_PROJECT_KEY = "projectKey"
KEY_ISSUE_TYPE = "issueType"
KEY_MAX_RESULT = "maxResult"
KEY_START_AT = "startAt"


class PayloadsBuilder(object):
    def __init__(self):
        self.payload = {}
        self.defaultSetting()

    def defaultSetting(self):
        self.payload["fieldsByKeys"] = False

    def withExpand(self, *args):
        self.payload["expand"] = []
        for arg in args:
            self.payload["expand"].append(arg)
        return self

    def withJQL(self, **args):
        count = 0
        self.payload["jql"] = ""
        for key, value in args.items():
            if count%2 == 0:
                self.payload["jql"] += "{} = `{}`".format(key, value)
            elif count%2 == 1 and key == "op" and ( value == "AND" or value == "OR"):
                self.payload["jql"] += " {} ".format(value)
            else:
                print("jql statement error")
            count += 1
        print(self.payload["jql"])
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
        return self.payload




# def payload(projectKey, issueType ,maxResults, startAt):
#     return json.dumps({
#         "expand": [
#             "changelog"
#         ],
#         "jql": "project = {projectKey} AND issueType = {issueType} AND status = 'In Progress'".format(projectKey = projectKey, issueType = issueType),
#         "maxResults": maxResults,
#         "fieldsByKeys": False,
#         "fields": ["*all"], 
#         # "fields" : ["issuetype", "summary", "created", "updated", "priority", "assignee", "creator", "reporter", "status", "timespent"],
#         "startAt": startAt
#     })



if __name__=="__main__":
    payloads = {
        KEY_PROJECT_KEY: "PJA", 
        KEY_ISSUE_TYPE: "Story",
        KEY_MAX_RESULT: 10,
        KEY_START_AT: 0
    }
    projectKey = "PJA"
    
    builder = PayloadsBuilder()

    payloads = builder\
        .withExpand("changelog")\
        .withFields("issuetype", "summary")\
        .withJQL(project="PJA", op="AND", issueType="Story")\
        .getPayloads()

    print(payloads)
