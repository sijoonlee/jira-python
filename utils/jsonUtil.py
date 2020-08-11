import json

def printResponseJson(data):
    print(json.dumps(data, indent=2))

def readFileReport(filename):
    data = None
    with open(filename) as file:
        data = json.load(file)
    return data

def writeFileReport(data, fileName):
    with open(fileName, 'w') as file:
        file.write(json.dumps(data, indent=2))