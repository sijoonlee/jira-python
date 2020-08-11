# Database model
model = {
    "name" : "Issue",
    "fields" : [
        {"name" : "id", "type" : "TEXT", "option" : "PRIMARY KEY" },
        {"name" : "key", "type" : "TEXT" },
        {"name" : "summary", "type" : "TEXT" },
        {"name" : "created", "type" : "TEXT" }, # store it as TEXT and parse it as Date/Time later
        {"name" : "updated", "type" : "TEXT" },
        {"name" : "issueTypeId", "type" : "TEXT" },
        {"name" : "priorityId", "type" : "TEXT" },
        {"name" : "statusId", "type" : "TEXT" },
        {"name" : "projectId", "type" : "TEXT" },
        {"name" : "creatorId", "type" : "TEXT" },
        {"name" : "reporterId", "type" : "TEXT" },
        {"name" : "assigneeId", "type" : "TEXT" },
        {"name" : "creatorName", "type" : "TEXT" },
        {"name" : "reporterName", "type" : "TEXT" },
        {"name" : "assigneeName", "type" : "TEXT" }
    ],
    "foreignKeys" : [
        {"name": "issueTypeId", "references": "IssueType(id)"},
        {"name": "projectId", "references": "Project(id)"},
        {"name": "priorityId", "references": "Priority(id)"},
        {"name": "statusId", "references": "Status(id)"},
        {"name": "creatorId", "references": "User(accountId)"},
        {"name": "reporterId", "references": "User(accountId)"},
        {"name": "assigneeId", "references": "User(accountId)"},
    ]
}

# Lookup table
# @key : Field name in Database
# @value: Field path in Jira response's json structure
lookup = {
    "id" : "id",
    "key" : "key",
    "summary" : "fields->summary",
    "created" : "fields->created",
    "updated" : "fields->updated",
    "issueTypeId" : "fields->issuetype->id",
    "priorityId" : "fields->priority->id",
    "statusId" : "fields->status->id",
    "projectId" : "fields->project->id",
    "creatorId" : "fields->creator->accountId",
    "reporterId" : "fields->reporter->accountId",
    "assigneeId" : "fields->assignee->accountId",
    "creatorName" : "fields->creator->displayName",
    "reporterName" : "fields->reporter->displayName",
    "assigneeName" : "fields->assignee->displayName",
}