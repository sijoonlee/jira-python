import json
from config import apiAddress
DEFAULT_FIELDS = [ "issuetype", "summary", "priority", "status", "project",
                   "created", "updated", # "timespent",
                   "assignee", "creator", "reporter"] # ["*all"] # to get all fields
DEFAULT_EXPAND = [] #["changelog"] # unnecessary for now

url = apiAddress + "/search"
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

    # args looks like
    #   "project" = "PJA" , 
    #   "op1" = "AND" ,
    #   "status" = "In Progress", 
    #   "op2" = "OR" ,     
    #   "project = "SP"
    def withJQL(self, **args):
        count = 0
        if len(args) > 0:
            self.payload["jql"] = ""

            for key, value in args.items():
                if count%2 == 0:
                    self.payload["jql"] += "{} = {}".format(key, value)
                elif count%2 == 1 and key.startswith("op") and ( value == "AND" or value == "OR"):
                    self.payload["jql"] += " {} ".format(value)
                else:
                    print("jql statement error")
                count += 1
        
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
        .withJQL(**jqlQuery)\
        .withPagination(maxResults, startAt)\
        .getPayloads()
    
    return payloads



if __name__=="__main__":
    
    jqlQuery = {"proejct":"PJA", "op1":"AND", "status":"Done"}
    
    builder = PayloadsBuilder()

    print(payloadGenerator(jqlQuery, 1, 0))
    