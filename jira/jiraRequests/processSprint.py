import re
from model import sprint

# Converting String-coded information to DB-ready object

def getMatchGroups(sprintString):    
    p = re.compile(sprint.pattern)
    obj = p.match(str(sprintString))
    if obj:
        return obj.groups()
    else:
        return None

def generateDBreadyData(sprintString):
    totalData = {}
    sprintData = {}
    groups = getMatchGroups(sprintString)
    if groups:
        for i in range(len(sprint.totalFields)):
            key = sprint.totalFields[i]
            value = groups[i]
            totalData[key] = value

        for field in sprint.selectedFields:
            sprintData[field] = totalData[field]

        for key, value in sprintData.items():
            if value == '<null>' or value == '':
                sprintData[key] = None
    return sprintData

def processSprint(responseObject):
    issuePath = sprint.lookup["issueId"]
    sprintPath = sprint.lookup["sprint"].split("->")
    
    sprintRecordList = []
    sprintIssueLinkRecordList = []

    for records in responseObject:
        issueId = None
        for level in issuePath:
            issueId = records.get(issuePath, None)

        for level in sprintPath:
            records = records.get(level, None)
            if records is None:
                break
            else:    
                for record in records:
                    sprintRecord = generateDBreadyData(record)
                    if len(sprintRecord) > 0:
                        sprintRecordList.append(sprintRecord)

        if issueId is not None and len(sprintRecordList) > 0:
            sprintIssueLinkRecord = {}
            sprintIssueLinkRecord["issueId"] = issueId
            for sprintRecord in sprintRecordList:
                sprintIssueLinkRecord["sprintId"] = sprintRecord["id"]
                sprintIssueLinkRecordList.append(sprintIssueLinkRecord)

    return sprintRecordList, sprintIssueLinkRecordList