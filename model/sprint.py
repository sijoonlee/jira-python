model = {
    "name" : "Sprint",
    "fields" : [
        {"name" : "id", "type" : "TEXT", "option" : "PRIMARY KEY" },
        {"name" : "name", "type" : "TEXT" },
        {"name" : "goal", "type" : "TEXT" },
        {"name" : "state", "type" : "TEXT" },
        {"name" : "startDate", "type" : "TEXT" },
        {"name" : "endDate", "type" : "TEXT" },
        {"name" : "completeDate", "type" : "TEXT" },
    ]
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