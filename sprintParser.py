import re

if __name__=="__main__":
    sprint1 = 'com.atlassian.greenhopper.service.sprint.Sprint@2d1cc666[completeDate=2020-08-11T13:40:59.447Z,endDate=2020-08-28T19:07:22.000Z,goal=,id=3,name=SP Sprint 1,rapidViewId=2,sequence=3,startDate=2020-08-07T19:07:29.401Z,state=CLOSED]'
    sprint2 = "com.atlassian.greenhopper.service.sprint.Sprint@284a84f2[completeDate=<null>,endDate=2020-09-01T13:41:07.000Z,goal=Test Custom Field,id=5,name=SP Sprint 2,rapidViewId=2,sequence=5,startDate=2020-08-11T13:41:17.461Z,state=ACTIVE]"
    pattern = 'com.atlassian.greenhopper.service.sprint.Sprint@(.*)\[completeDate=(.*),endDate=(.*),goal=(.*),id=(.*),name=(.*),rapidViewId=(.*),sequence=(.*),startDate=(.*),state=(.*)\]'
    p = re.compile(pattern)
    obj = p.match(str(sprint1))
        
    totalData = {}
    totalFields = ["identifier", "completeDate", "endDate", "goal", "id", "name", "rapidViewId", "sequence", "startDate", "state"]
    selectedFields = ["id", "name", "goal",  "state", "startDate", "endDate", "completeDate"]
    sprintData = {}

    for i in range(len(totalFields)):
        key = totalFields[i]
        value = obj.groups()[i]
        totalData[key] = value

    for field in selectedFields:
        sprintData[field] = totalData[field]

    for key, value in sprintData.items():
        if value == '<null>' or value == '':
            sprintData[key] = None

    print(sprintData)