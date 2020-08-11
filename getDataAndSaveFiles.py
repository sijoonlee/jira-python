from jira.jiraRequests.projects import getProjectPagination, getAllProjects
from jira.jiraRequests.issueTypes import getIssueTypes
from jira.jiraRequests.statuses import getStatuses
from jira.jiraRequests.issues import getIssuesPagination, getAllIssues
from jira.jiraRequests.users import getAllUsers
from jira.jiraRequests.priorities import getPriorities
from utils.jsonUtil import writeFileReport


if __name__=="__main__":
       
    data = getAllProjects()
    writeFileReport(data, "./exampleResponse/getAllProjects.json")
    
    data = getIssueTypes()
    writeFileReport(data, "./exampleResponse/getIssueTypes.json")

    data = getStatuses()
    writeFileReport(data, "./exampleResponse/getStatuses.json")

    data = getAllIssues()
    writeFileReport(data, "./exampleResponse/getAllIssues.json")

    data = getAllUsers()
    writeFileReport(data, "./exampleResponse/getAllUsers.json")

    data = getPriorities()
    writeFileReport(data, "./exampleResponse/getPriorites.json")