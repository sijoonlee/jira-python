from table.table import Table

class SprintIssueLink(Table):
    model = {
        "name" : "SprintIssueLink",
        "fields" : [
            {"name" : "sprintId", "type" : "TEXT" },
            {"name" : "issueId", "type" : "TEXT" }
        ],
        "primaryKeys" : [ "sprintId", "issueId" ]#,
        # "foreignKeys" : [
        #     {"name": "sprintId", "references": "Sprint(id)"},
        #     {"name": "issueId", "references": "Issue(id)"},
        # ]
    }

    lookup = {
        "issueId":"id"
    }
    # sprintId will be inserted in other way since our response(getAllIssuesInSprint) doesn't have sprint information
    # check update method in dbActions under businessLogic

