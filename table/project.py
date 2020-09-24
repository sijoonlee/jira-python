from table.table import Table

class Project(Table):
    model = {
        "name": "Project",
        "fields": [
            {"name": "id", "type": "TEXT", "option": "PRIMARY KEY"},
            {"name": "key", "type": "TEXT"},
            {"name": "name", "type": "TEXT"},
            {"name": "style", "type": "TEXT"}
        ]   
    }

    # Lookup table
    # @key : Field name in Database
    # @value: Field path in Jira response's json structure
    lookup = {
        "id" : "id",
        "key" : "key",
        "name" : "name",
        "style" : "style"
    }
