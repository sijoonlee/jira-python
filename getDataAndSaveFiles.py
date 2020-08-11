from jiraRequests.projects import getProjectPagination, getAllProjects
from jiraRequests.issueTypes import getIssueTypes
from jiraRequests.statuses import getStatuses
from jiraRequests.issues import getIssuesPagination, getAllIssues
from jiraRequests.users import getAllUsers
from jiraRequests.priorities import getPriorities
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