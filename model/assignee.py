model = {
    "name" : "Assignee",
    "fields" : [
        {"name" : "issueId", "type" : "TEXT", "option" : "PRIMARY KEY" },
        {"name" : "userId", "type" : "TEXT", "option" : "PRIMARY KEY" }
    ],
    "foreignKeys" : [
        {"name": "issueId", "references": "Issue(id)"},
        {"name": "userId", "references": "User(accountId)"}
    ]
}