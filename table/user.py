from table.table import Table

class User(Table):
    model = {
        "name" : "Users", # table name, 'user' is reserved name in Postgres
        "fields" : [
            {"name" : "accountId", "type" : "TEXT", "option" : "PRIMARY KEY" },
            {"name" : "accountType", "type" : "TEXT" },
            {"name" : "emailAddress", "type" : "TEXT" },
            {"name" : "displayName" , "type" : "TEXT" },
            {"name" : "active", "type" : "BOOLEAN"} # caution: SQLite doesn't have boolean 0(false), 1(true)
        ]
    }

    lookup = {
        "accountId" : "accountId",
        "accountType" : "accountType",
        "emailAddress" : "emailAddress",
        "displayName" : "displayName",
        "active" : "active"
    }
