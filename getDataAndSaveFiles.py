from jira.jiraRequests.projects import getProjectPagination, getAllProjects
from jira.jiraRequests.issueTypes import getIssueTypes
from jira.jiraRequests.statuses import getStatuses
from jira.jiraRequests.issues import getIssuesPagination, getAllIssues
from jira.jiraRequests.users import getAllUsers
from jira.jiraRequests.priorities import getPriorities
from jira.jiraRequests.boards import getAllBoards
from jira.jiraRequests.sprints import getAllSprintsInBoard, getSprintsInBoardPagination
from jira.jiraRequests.issuesInSprint import getAllIssuesInSprint
from utils.jsonUtil import writeFileReport


if __name__=="__main__":
       
    #dir = 'exampleResponse'
    dir = 'ratehubResponse'
    """
    data = getAllProjects()
    writeFileReport(data, "./{}/getAllProjects.json".format(dir))
    
    data = getIssueTypes()
    writeFileReport(data, "./{}/getIssueTypes.json".format(dir))

    data = getStatuses()
    writeFileReport(data, "./{}/getStatuses.json".format(dir))

    data = getAllIssues()
    writeFileReport(data, "./{}/getAllIssues.json".format(dir))

    data = getAllUsers()
    writeFileReport(data, "./{}/getAllUsers.json".format(dir))

    data = getPriorities()
    writeFileReport(data, "./{}/getPriorites.json".format(dir))

    data = getAllBoards()
    writeFileReport(data, "./{}/getAllBoards.json".format(dir))

    data = getSprintsInBoardPagination(1,10,0) # board id 1
    writeFileReport(data, "./{}/getSprintsInBoardPagination.json".format(dir))
    """
    data = getAllSprintsInBoard("40") # board id
    writeFileReport(data, "./{}/getAllSprintsInBoard.json".format(dir))

    data = getAllIssuesInSprint("40", "11") # board id, sprint id
    writeFileReport(data, "./{}/getAllIssuesInSprint.json".format(dir))