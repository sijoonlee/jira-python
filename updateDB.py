import re
from datetime import date
from db.sqlite3.connector import SqliteConnector
from db.postgres.connector import PostgresConnector
from jira.jiraRequests.responseProcessor import responseProcessor
from businessLogic.db.dbActions import DbActions
from utils.jsonUtil import writeFileReport, readFileReport
import time

# this is to fetch those data created/updated after a certain date
if __name__=="__main__":
    #dbActions.reset(PostgresConnector)
    dbActions = DbActions(SqliteConnector, responseProcessor)

    dbActions.reset()
    print("The whole process would take around 10 ~ 30 min")
    start_time = time.time()
    # dbActions.updateUsingAgileApi(SqliteConnector, responseProcessor)
    dbActions.update()
    # dbActions.update(PostgresConnector, responseProcessor)
    # dbActions.updateUsingAgileApi(PostgresConnector, responseProcessor)
    duration = time.time() - start_time 
    print("time spent (min):", int(duration/60))