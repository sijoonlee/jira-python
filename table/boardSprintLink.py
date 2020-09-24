from table.table import Table

class BoardSprintLink(Table):
    model = {
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

    lookup = {
        "sprintId":"id"
    }