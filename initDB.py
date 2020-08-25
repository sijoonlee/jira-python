from db.sqlite3.connector import SqliteConnector
from jira.jiraRequests.responseProcessor import responseProcessor
from businessLogic.db import dbActions
from datetime import date
from utils.jsonUtil import writeFileReport
from config import config
import time

# this is to reset and get all data from start
if __name__=="__main__":

    print("The whole process would take around 10 min")
    start_time = time.time()

    dbConnector = SqliteConnector(config["dbFile"])
    dbActions.reset(dbConnector)

    since = "2014-06-17" # the first date of Ratehub's Jira data
    to = date.today()
    info = "Last update: Data since [{since}] to [{to}]".format(since=since, to=to)
    writeFileReport(info, "./update-info.md")
    dbActions.update(dbConnector, responseProcessor, since)

    duration = time.time() - start_time 
    print("time spent:", duration)
