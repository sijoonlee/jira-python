from utils.jsonUtil import readFileReport
from db.postgres.connector import PostgresConnector

if __name__=="__main__":
    connector = PostgresConnector()
    
    records = readFileReport("./sprintissuelink.json")

    model1 = {
        "name" : "SprintIssueLink",
        "fields" : [
            {"name" : "sprintId", "type" : "TEXT" },
            {"name" : "issueId", "type" : "TEXT" }
        ],
        "primaryKeys" : [ "sprintId", "issueId" ]#,
        # "foreignKeys" : [
        #     {"name": "sprintId", "references": "Sprint(id)"},
        #     {"name": "issueId", "references": "Issue(id)"},
    }

    model2 = {
        "name" : "BoardSprintLink",
        "fields" : [
            {"name" : "boardId", "type" : "TEXT" },
            {"name" : "sprintId", "type" : "TEXT" }
        ],
        "primaryKeys" : [ "boardId", "sprintId" ]#,
        # "foreignKeys" : [
        #     {"name": "sprintId", "references": "Sprint(id)"},
        #     {"name": "issueId", "references": "Issue(id)"},
        # ]
    }
    connector.insertRecords(model, records)
