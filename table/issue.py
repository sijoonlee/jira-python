# Database model
model = {
    "name" : "Issue",
    "fields" : [
        {"name" : "id", "type" : "TEXT", "option" : "PRIMARY KEY" },
        {"name" : "key", "type" : "TEXT" },
        {"name" : "summary", "type" : "TEXT" },
        {"name" : "storyPoints", "type" : "REAL" },
        {"name" : "created", "type" : "TIMESTAMPTZ" },
        {"name" : "updated", "type" : "TIMESTAMPTZ" },
        {"name" : "resolutionId", "type" : "TEXT" },
        {"name" : "resolutionDate", "type" : "TIMESTAMPTZ" },
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
    ]#,
    # "foreignKeys" : [
    #     {"name": "issueTypeId", "references": "IssueType(id)"},
    #     {"name": "projectId", "references": "Project(id)"},
    #     {"name": "priorityId", "references": "Priority(id)"},
    #     {"name": "statusId", "references": "Status(id)"},
    #     {"name": "resolutionId", "references": "Resolution(id)"},
    #     {"name": "creatorId", "references": "Users(accountId)"},
    #     {"name": "reporterId", "references": "Users(accountId)"},
    #     {"name": "assigneeId", "references": "Users(accountId)"},
    #     {"name": "leadDevId", "references": "Users(accountId)"},
    #     {"name": "leadQAId", "references": "Users(accountId)"}
    # ]
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
    "resolutionId" : "fields->resolution->id",
    "resolutionDate" : "fields->resolutiondate",
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
    "leadDevName" : "fields->customfield_10820->displayName",
    "leadQAName" : "fields->customfield_10821->displayName"
}

def drop(dbConnector):
    dbConnector.dropTable(model)

def create(dbConnector):
    dbConnector.createTable(model)

def update(dbConnector, responseProcessor, response, injection={}):
    dbReadyData = responseProcessor(lookup, response, injection)
    dbConnector.insertRecords(model, dbReadyData)
    return dbReadyData

def updateUsingDbReadyData(dbConnector, dbReadyData):
    dbConnector.insertRecords(model, dbReadyData)
    return dbReadyData

def getDbReadyData(responseProcessor, response, injection={}):
    return responseProcessor(lookup, response, injection)