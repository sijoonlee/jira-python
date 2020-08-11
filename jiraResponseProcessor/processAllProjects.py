from db.sqlite3.model import project

def process(response):

    fields = list(project.model.keys())
    processedRecords = []
    for item in response:
        record = {}
        for field in fields:
            record[field] = item[field]
        processedRecords.append(record)
    return processedRecords
