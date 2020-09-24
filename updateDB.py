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
    
    # DbActions
    # @param: ClassDbConnector
    #    Use PostgresConnector or RedshiftConnector
    # @param: responseProcessor
    #    Use responseProcessor, 
    #    responseProcessor is responsible for organizing raw data from Jira to get ready for Database
    # @param: maxWorkers
    #    # of threads for fetching data from Jira API
    dbActions = DbActions(RedshiftConnector, responseProcessor, maxWorkers=4)
    
    # this will drop all tables and create them again
    # dbActions.reset()

    print("Total Time would take")
    print("-- 3 ~ 20 min when using local PostgreSQL")
    print("-- around 40 min when using Amazon Redshift")
    print("(cf) The fetching data from Jira would take around 2~10 min depending on # of workers")
    print(" By default, # of workers = 4, fetching would take 2 min")
    start_time = time.time()
    dbActions.update()
    duration = time.time() - start_time 
    print("time spent (min):", int(duration/60))