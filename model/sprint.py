model = {
    "name" : "Sprint",
    "fields" : [
        {"name" : "id", "type" : "TEXT", "option" : "PRIMARY KEY" },
        {"name" : "name", "type" : "TEXT" },
        {"name" : "goal", "type" : "TEXT" },
        {"name" : "state", "type" : "TEXT" },
        {"name" : "startDate", "type" : "TEXT" },
        {"name" : "endDate", "type" : "TEXT" },
        {"name" : "completeDate", "type" : "TEXT" },
    ]
}


# Lookup info
lookup = {"issueId":"id", "sprint":"fields->customfield_10020"}
totalFields = ["identifier", "completeDate", "endDate", "goal", "id", "name", "rapidViewId", "sequence", "startDate", "state"]
selectedFields = ["id", "name", "goal",  "state", "startDate", "endDate", "completeDate"]
pattern = 'com.atlassian.greenhopper.service.sprint.Sprint@(.*)\[completeDate=(.*),endDate=(.*),goal=(.*),id=(.*),name=(.*),rapidViewId=(.*),sequence=(.*),startDate=(.*),state=(.*)\]'