# Database model
model = {
    "name" : "Issue",
    "fields" : [
        {"name" : "id", "type" : "TEXT", "option" : "PRIMARY KEY" },
        {"name" : "key", "type" : "TEXT" },
        {"name" : "summary", "type" : "TEXT" },
        {"name" : "storyPoints", "type" : "TEXT" }, # Tried READ first, but make trouble, rather parse it later
        {"name" : "created", "type" : "TEXT" }, # store it as TEXT and parse it as Date/Time later
        {"name" : "updated", "type" : "TEXT" },
        {"name" : "parentId", "type" : "TEXT" },
        {"name" : "parentKey", "type" : "TEXT" },
        {"name" : "parentSummary", "type" : "TEXT" },
        {"name" : "issueTypeId", "type" : "TEXT" },
        {"name" : "priorityId", "type" : "TEXT" },
        {"name" : "statusId", "type" : "TEXT" },
        {"name" : "projectId", "type" : "TEXT" },
        {"name" : "creatorId", "type" : "TEXT" },
        {"name" : "creatorName", "type" : "TEXT" },
        {"name" : "reporterId", "type" : "TEXT" },
        {"name" : "reporterName", "type" : "TEXT" },
        {"name" : "assigneeId", "type" : "TEXT" },
        {"name" : "assigneeName", "type" : "TEXT" },
        {"name" : "leadDevId", "type" : "TEXT" },
        {"name" : "leadDevName", "type" : "TEXT" },
        {"name" : "leadQAId", "type" : "TEXT" },
        {"name" : "leadQAName", "type" : "TEXT" }
    ],
    "foreignKeys" : [
        {"name": "issueTypeId", "references": "IssueType(id)"},
        {"name": "projectId", "references": "Project(id)"},
        {"name": "priorityId", "references": "Priority(id)"},
        {"name": "statusId", "references": "Status(id)"},
        {"name": "creatorId", "references": "User(accountId)"},
        {"name": "reporterId", "references": "User(accountId)"},
        {"name": "assigneeId", "references": "User(accountId)"},
        {"name": "leadDevId", "references": "User(accountId)"},
        {"name": "leadQAId", "references": "User(accountId)"}
    ]
}

# Lookup table
# @key : Field name in Database
# @value: Field path in Jira response's json structure
lookup = {
    "id" : "id",
    "key" : "key",
    "summary" : "fields->summary",
    "storyPoints":"fields->customfield_10004",
    "created" : "fields->created",
    "updated" : "fields->updated",
    "parentId" : "fields->parent->id",
    "parentKey" : "fields->parent->key",
    "parentSummary" : "fields->parent->fields->summary",
    "issueTypeId" : "fields->issuetype->id",
    "priorityId" : "fields->priority->id",
    "statusId" : "fields->status->id",
    "projectId" : "fields->project->id",
    "creatorId" : "fields->creator->accountId",
    "reporterId" : "fields->reporter->accountId",
    "assigneeId" : "fields->assignee->accountId",
    "leadDevId" : "fields->customfield_10820->accountId",
    "leadQAId" : "fields->customfield_10821->accountId",
    "creatorName" : "fields->creator->displayName",
    "reporterName" : "fields->reporter->displayName",
    "assigneeName" : "fields->assignee->displayName",
    "leadDevId" : "fields->customfield_10820->displayName",
    "leadQAId" : "fields->customfield_10821->displayName"
}