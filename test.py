from jiraRequests.getProjects import getProjectPagination, getAllProjects
from jiraRequests.getIssueTypes import getIssueTypes
from jiraRequests.getStatuses import getStatuses
from jiraRequests.getIssues import getIssuesPagination, getAllIssues
from jiraRequests.getUsers import getAllUsers
from jiraRequests.getPriorities import getPriorities
from utils.jsonUtil import writeFileReport


if __name__=="__main__":
       
    data = getAllProjects()
    writeFileReport(data, "getAllProjects.json")
    
    data = getIssueTypes()
    writeFileReport(data, "getIssueTypes.json")

    data = getStatuses()
    writeFileReport(data, "getStatuses.json")

    data = getAllIssues()
    for issue in data:
        reporter = issue["fields"].get("reporter", None)
        reporterEmailAddress = ""
        reporterDisplayName = ""
        if reporter is not None:
            reporterEmailAddress= reporter["emailAddress"]
            reporterDisplayName = reporter["displayName"]
        
        assignee = issue["fields"].get("assignee", None)
        assigneeEmailAddress = ""
        assigneeDisplayName = ""
        if assignee is not None:
            assigneeEmailAddress= assignee["emailAddress"]
            assigneeDisplayName = assignee["displayName"]

        print(issue["id"], issue["key"], issue["fields"]["summary"],\
            issue["fields"]["issuetype"]["id"], issue["fields"]["issuetype"]["name"],\
            "reporter", reporterEmailAddress, reporterDisplayName,\
            "assignee", assigneeEmailAddress, assigneeDisplayName)
    writeFileReport(data, "getAllIssues.json")

    data = getAllUsers()
    writeFileReport(data, "getAllUsers.json")

    data = getPriorities()
    writeFileReport(data, "getPriorites.json")