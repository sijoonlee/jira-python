model = {
    "name" : "Board",
    "fields" : [
        { "name": "id", "type": "TEXT", "option" : "PRIMARY KEY" },
        { "name": "name" , "type": "TEXT"},
        { "name": "type", "type": "TEXT"},
        { "name": "projectId", "type": "TEXT"}
    ]
}

# Lookup table
# @key : Field name in Database
# @value: Field path in Jira response's json structure
lookup = {
    "id" : "id",
    "name" : "name",
    "type" : "type",
    "projectId" : "location->projectId"
}