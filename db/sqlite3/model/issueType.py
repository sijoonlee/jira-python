model = {
    "name" : "IssueType",
    "fields" : [
        {"name" : "id", "type" : "TEXT", "option" : "PRIMARY KEY" },
        {"name" : "name", "type" : "TEXT" },
        {"name" : "projectId", "type" : "TEXT" }
    ],
    "foreignKeys" : [
        {"name": "projectId", "references": "Project(id)"}
    ]
}