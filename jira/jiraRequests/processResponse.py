from model import issue

# Converting HTTP Response to DB-ready object

def findValue(responseObject, path):
    path = path.split("->")
    value = responseObject
    for level in path:
        value = value.get(level, None)
        if value is None:
            break
    return value

# response is an array of multiple items
# [ {"id":"1000", "name":"example1"}, ... ]
def processResponse(lookup, response):

    fieldNames = list(lookup.keys())
    pathsInResponse = list(lookup.values())

    dbReadyRecordList = []
    for entity in response:
        dbReadyRecord = {}
        for i in range(len(fieldNames)):
            field = fieldNames[i]
            path = pathsInResponse[i]
            dbReadyRecord[field] = findValue(entity, path)
        dbReadyRecordList.append(dbReadyRecord)
    return dbReadyRecordList