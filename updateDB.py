import re
from datetime import date
from db.postgres.connector import PostgresConnector
from db.redshift.connector import RedshiftConnector
from jira.jiraRequests.responseProcessor import responseProcessor
from businessLogic.db.dbActions import DbActions
from utils.jsonUtil import writeFileReport, readFileReport
import time

# this is to fetch those data created/updated after a certain date
if __name__=="__main__":
    # use database connector you want to use - PostgresConnector, RedshiftConnector
    dbActions = DbActions(PostgresConnector, responseProcessor, maxWorkers=4)
    dbActions.reset()

    print("The fetching process would take around 2~10 min depending on # of workers")
    print("Fetching default: 4 workers, about 2~3 min")
    print("-------------------------------------------------------")
    print("The updating Amazon Redshift database with the lowest setting of CPU would take around 70 min")
    print("The updating local Postgres database would take less than 1 min")
    start_time = time.time()
    dbActions.update()
    duration = time.time() - start_time 
    print("time spent (min):", int(duration/60))