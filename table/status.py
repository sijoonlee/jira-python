from table.table import Table

class Status(Table):

    model = {
        "name": "Status",
        "fields": [
            {"name": "id", "type": "TEXT", "option": "PRIMARY KEY"},
            {"name": "name", "type": "TEXT"},
            {"name": "description", "type": "TEXT"},
            {"name": "projectId", "type": "TEXT"},
        ]#,
        # "foreignKeys" : [
        #     {"name": "projectId", "references": "Project(id)"}
        # ]
    }

    # Lookup table
    # @key : Field name in Database
    # @value: Field path in Jira response's json structure
    lookup = {
        "id" : "id",
        "name" : "name",
        "description" : "description",
        "projectId" : "scope->project->id"
    }

