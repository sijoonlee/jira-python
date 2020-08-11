model = {
    "name" : "SprintIssueLink",
    "fields" : [
        {"name" : "sprintId", "type" : "TEXT" },
        {"name" : "issueId", "type" : "TEXT" }
    ],
    "primaryKeys" : [ "sprintId", "issueId" ],
    "foreignKeys" : [
        {"name": "sprintId", "references": "Sprint(id)"},
        {"name": "issueId", "references": "Issue(id)"},
    ]
}