import re
from datetime import date
from db.sqlite3.connector import SqliteConnector
from jira.jiraRequests.responseProcessor import responseProcessor
from businessLogic.db import dbActions
from utils.jsonUtil import writeFileReport, readFileReport

# this is to fetch those data created/updated after a certain date
if __name__=="__main__":
    dbFile = './db/sqlite3/storage/db.sqlite'
    dbConnector = SqliteConnector(dbFile)

    # Change this value
    since = "2020-08-10"

    to = date.today()
    info = "Last update: Data since [{since}] to [{to}]".format(since=since, to=to)
    writeFileReport(info, "./update-info.md")
    #dbActions.update(dbConnector, responseProcessor, since)
    readInfo = readFileReport("./update-info.md")
    x = re.search("^The.*Spain$", readInfo) 