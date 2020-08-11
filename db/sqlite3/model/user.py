model = {
    "name" : "User", # table name
    "fields" : [
        {"name" : "accountId", "type" : "TEXT", "option" : "PRIMARY KEY" },
        {"name" : "accountType", "type" : "TEXT" },
        {"name" : "emailAddress", "type" : "TEXT" },
        {"name" : "displayName" , "type" : "TEXT" },
        {"name" : "active", "type" : "INTEGER"} # SQLite doesn't have boolean 0(false), 1(true)
    ]
}