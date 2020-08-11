model = {
    "name": "Status",
    "fields": [
        {"name": "id", "type": "TEXT", "option": "PRIMARY KEY"},
        {"name": "name", "type": "TEXT"},
        {"name": "description", "type": "TEXT"},
        {"name": "projectId", "type": "TEXT"},
    ],
    "foreignKeys" : [
        {"name": "projectId", "references": "Project(id)"}
    ]
}