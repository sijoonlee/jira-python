from db.sqlite3.connector import SqliteConnector
from businessLogic.db import dbActions

if __name__=="__main__":
    dbFile = './db/sqlite3/storage/db.sqlite'
    dbConnector = SqliteConnector(dbFile)
    #dbActions.reset(dbConnector)
    dbActions.update(dbConnector)
