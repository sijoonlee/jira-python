import re
from datetime import date
from db.sqlite3.connector import SqliteConnector
from jira.jiraRequests.responseProcessor import responseProcessor
from businessLogic.db import dbActions
from utils.jsonUtil import writeFileReport, readFileReport

# this is to fetch those data created/updated after a certain date
if __name__=="__main__":

    readInfo = readFileReport("./update-info.md")
    print("Read from update-info.md - ", str(readInfo))
    pattern = "Last update: Data since \[(.*)\] to \[(.*)\]"
    compiledPattern = re.compile(pattern)
    subMatches = compiledPattern.match(str(readInfo)).groups()
    since = subMatches[1]
    to = date.today()

    print("Update data since [{since}] to [{to}]".format(since=since, to=to))
    writeFileReport("Last update: Data since [{since}] to [{to}]".format(since=since, to=to), "./update-info.md")

    dbFile = './db/sqlite3/storage/db.sqlite'
    dbConnector = SqliteConnector(dbFile)
    dbActions.update(dbConnector, responseProcessor, since)
