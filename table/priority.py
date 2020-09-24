from table.table import Table

class Priority(Table):
    model = {
        "name" : "Priority",
        "fields" : [
            { "name": "id", "type": "TEXT", "option" : "PRIMARY KEY" },
            { "name": "name" , "type": "TEXT"},
            { "name": "description", "type": "TEXT"}
        ]
    }

    # Lookup table
    # @key : Field name in Database
    # @value: Field path in Jira response's json structure
    lookup = {
        "id" : "id",
        "name" : "name",
        "description" : "description"
    }
