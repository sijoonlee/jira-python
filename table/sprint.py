from table.table import Table

class Sprint(Table):
    model = {
        "name" : "Sprint",
        "fields" : [
            {"name" : "id", "type" : "TEXT", "option" : "PRIMARY KEY" },
            {"name" : "name", "type" : "TEXT" },
            {"name" : "goal", "type" : "TEXT" },
            {"name" : "state", "type" : "TEXT" },
            {"name" : "startDate", "type" : "TIMESTAMPTZ" },
            {"name" : "endDate", "type" : "TIMESTAMPTZ" },
            {"name" : "completeDate", "type" : "TIMESTAMPTZ" }
        ]#,
        # "foreignKeys" : [
        #     {"name": "boardId", "references": "Board(id)"}
        # ]
    }

    lookup = {
        "id":"id",
        "name":"name",
        "goal":"goal",
        "state":"state",
        "startDate":"startDate",
        "endDate":"endDate",
        "completeDate":"completeDate"
    }
