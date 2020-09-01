import re
from datetime import date
from db.sqlite3.connector import SqliteConnector
from jira.jiraRequests.responseProcessor import responseProcessor
from businessLogic.db import dbActions
from utils.jsonUtil import writeFileReport, readFileReport
import time

# this is to fetch those data created/updated after a certain date
if __name__=="__main__":

    print("The whole process would take around 5 ~ 10 min")
    start_time = time.time()
    # dbActions.updateUsingAgileApi(SqliteConnector, responseProcessor)
    dbActions.update(SqliteConnector, responseProcessor)
    duration = time.time() - start_time 
    print("time spent (min):", int(duration/60))