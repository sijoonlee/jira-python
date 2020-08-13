from businessLogic.metrics import issueType
from businessLogic.metrics import storyPoints
from businessLogic.metrics import sprint

import datetime
from datetime import timezone

if __name__=="__main__":
    
    # str1 = '\'Improve test\''
    # print(str1)
    # str2  = str1.replace("'", "''")    
    # print(str2)

    # print(issueType.getMetricsPerProject("OMP"))
    #print(storyPoints.getMetricsPerProject("OMP"))

    # storyPoints.findIssuesCreatedBetween('OMP', '2020-05-11', '2020-05-25')
    #storyPoints.issuesInSprint("431")
    # sprint.numberOfIssuesInSprint("74", "497")

    # omp 1932 // OMP May 11 - May 25, 2020 // 93, 431
    # omp 1824 // OMP Apr 13 - Apr 26       // 93, 425
    # omp 1893 // OMP Jan 20 - Feb 3        // 93, 420
    # ok       // OMP Dec 23, 2019 - Jan 2  // 93, 408

    # Core - Sprint 95  (Core Mortgage)
    # Burnup chart has 13 issues
    # 
    # CORE-327 / CORE-410 were not included by my code
    # CORE-773 / CORE-863 / CORE-880 / CORE-908 is not shown in Burnup Chart

    #sprint.pivotCountIssues("93", "2020-01-01", "2020-06-01")

    #sprint.pivotSumStoryPoints("93", "2020-01-01", "2020-06-01")


    sprint.calculateWorkDonePercentage("93", "2020-01-01", "2020-06-01")