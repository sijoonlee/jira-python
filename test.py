from businessLogic.metrics import issueType
from businessLogic.metrics import storyPoints

if __name__=="__main__":

    # str1 = '\'Improve test\''
    # print(str1)
    # str2  = str1.replace("'", "''")    
    # print(str2)

    # print(issueType.getMetricsPerProject("OMP"))
    print(storyPoints.getMetricsPerProject("OMP"))