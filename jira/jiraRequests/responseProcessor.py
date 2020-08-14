from table import issue

# Converting HTTP Response to DB-ready object

def findValue(responseObject, path):
    path = path.split("->")
    value = responseObject
    for level in path:
        value = value.get(level, None)
        if value is None:
            break
    return value

# @param: response - an array of multiple items
# [ {"id":"1000", "name":"example1"}, ... ]
# @param: injection - a dictionary to add (key,value) into dbReadyRecord
def responseProcessor(lookup, response, injection={}):

    fieldNames = list(lookup.keys())
    pathsInResponse = list(lookup.values())

    dbReadyRecordList = []
    for entity in response:
        dbReadyRecord = {**injection}
        for i in range(len(fieldNames)):
            field = fieldNames[i]
            path = pathsInResponse[i]
            dbReadyRecord[field] = findValue(entity, path)
        dbReadyRecordList.append(dbReadyRecord)
    return dbReadyRecordList