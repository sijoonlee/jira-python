import psycopg2
import os
import sys
import pandas as pd
from config import config

class PostgresConnector(object):
    def __init__(self):
        self.connection = psycopg2.connect(dbname=config["postgresDbName"],
                                            host=config["postgresHost"], 
                                            port=config["postgresPort"], 
                                            user=config["postgresUser"], 
                                            password=config["postgresPassword"])
        self.cur = self.connection.cursor()
    
    def __del__(self):
        self.connection.close()
        
    def dropTableStatement(self, model):
        return "DROP TABLE IF EXISTS {tableName} ".format(tableName = model["name"])

    def createTableStatement(self, model):
        statement = 'CREATE TABLE IF NOT EXISTS {tableName}'.format(tableName = model["name"])
        statement += "("
        for i in range(len(model["fields"])):
            fieldName = model["fields"][i]["name"]
            fieldType = model["fields"][i]["type"]
            fieldOption = model["fields"][i].get("option", None)
            statement += '{name} {type}'.format(name=fieldName,type=fieldType)
            if fieldOption is not None:
                statement += ' {}'.format(fieldOption)
            if i < len(model["fields"]) - 1 :
                statement += ','
        
        primaryKeys = model.get("primaryKeys", None)
        if primaryKeys is not None:
            statement += ',PRIMARY KEY (' + ','.join(primaryKeys) + ')'

        foreignKeys = model.get("foreignKeys", None)
        if foreignKeys is not None:
            statement += ','
            foreignKeyStmtArray = [ "FOREIGN KEY ({name}) REFERENCES {references}"\
                    .format(name=field["name"], references=field["references"])\
                    for field in foreignKeys]
            statement += ','.join(foreignKeyStmtArray)
        statement += ")"
        
        return statement

    def findTypeFromFieldName(self, model, fieldName):
        fieldType = None
        for field in model["fields"]:
            if field["name"] == fieldName:
                fieldType = field["type"]
                break
        return fieldType

    def findPrimaryKey(self, model):
        primaryKeys = set() # set

        if model.get('primaryKeys', None) != None:
            primaryKeys = {*model['primaryKeys']}
            
        if model.get("fields", None) != None:
            fields = model["fields"]
            for field in fields:
                if field.get("option", None) == 'PRIMARY KEY':
                    primaryKeys.add(field["name"])
                    
        return list(primaryKeys) # array

    # @param : fields 
    # key is field name, value is the value for the field
    # { "accountId" : "account0001", "accountType" : "saving" }
    def insertValuesStatement(self, model, record):
        
        fieldNames = list(record.keys())
        fieldValues = list(record.values())
        indexesToBeDeleted = []
        
        # this connector supports only 3 types for now: integer, real, text
        for i in range(len(fieldNames)):
            fieldType = self.findTypeFromFieldName(model, fieldNames[i])
            
            if fieldValues[i] != None:
                if fieldType is "INTEGER" or fieldType is "REAL" or fieldType is "BOOLEAN":
                    fieldValues[i] = str(fieldValues[i])
                elif fieldType is "TEXT":
                    # single, double quotes are escaped
                    # in sqlite you can escape by using ""(two double quotes) , ''(two sing quotes)
                    escaped = str(fieldValues[i]).replace("'", "''").replace('"', '""') #.replace('\n', ' ').replace('\r', '')
                    fieldValues[i] = "'{}'".format(escaped)
                else:
                    print("Error - Unknown type: ", fieldType)
            else:
                # This is to delete the field when the value is null
                indexesToBeDeleted.append(i) 
        
        # Delete null values, Database can use default value, or null value by its setting
        indexesToBeDeleted.sort(reverse=True)
        for i in indexesToBeDeleted:
            fieldNames.pop(i)
            fieldValues.pop(i)

        primaryKeys = self.findPrimaryKey(model)
        nonPrimaryKeyFields = [name for name in fieldNames if name not in primaryKeys]
        primaryKeys = ','.join(primaryKeys)
        fieldNames = ','.join(fieldNames)
        fieldValues = ','.join(fieldValues)
    
        statement = 'insert into {table} ({fieldNames}) values ({fieldValues})'\
            .format(table=model["name"], fieldNames=fieldNames, fieldValues=fieldValues)
        
        # if there are no fields other than primary key(s), nothing to update
        if len(nonPrimaryKeyFields) > 0 :
            statement += ' on conflict ({primaryKeys}) do update set '.format(primaryKeys=primaryKeys)
            setClauseArray = ['{field} = excluded.{field}'.format(field=field) for field in nonPrimaryKeyFields]
            setClause = ','.join(setClauseArray)
            statement += setClause
    
        return statement

    # @param: selectedFields - list of fields that are to be returned ex) ["id", "name", "creator"]
    # @param: whereClause - dictionary of fields that will be used in where clause 
    def queryTableStatement(self, selectedFieldNames, tableName, whereClause):
        
        selectedFieldNames = ",".join(selectedFieldNames)

        statement = 'select {fieldNames} from {table}'.format(fieldNames=selectedFieldNames, table=tableName)
        if whereClause is not None:
            statement += ' where {}'.format(whereClause)

        return statement

    
    # @param: selctedFields:list - ["tracks.albumid", "albums.title"]
    # @param: baseTable:string - "tracks"
    # @param: joinClauses:list of dict - [{"type":"INNER", "tableName":"albums", "onClause":"albums.albumid = tracks.albumid"}]
    # @param: whereClause:string - 'albums.albumid = "1" OR albums.albumid = "2"'
    # Example
    # SELECT
    #    tracks.ambumid, albums.title
    # FROM
    #    tracks
    #    INNER JOIN albums ON albums.albumid = tracks.albumid
    # WHERE
    #    albums.albumid = "1" OR albums.albumid = "2"

    def queryFromJoinStatement(self, selectedFields, tableName, joinClauses, whereClause):
        selectedFields = ','.join(selectedFields)
        statement = ' SELECT {}'.format(selectedFields)
        statement += ' FROM {}'.format(tableName)
        for joinClause in joinClauses:    
            statement += ' {joinType} JOIN {tableName} ON {onClause}'\
                .format(joinType=joinClause["type"], tableName=joinClause["tableName"], onClause=joinClause["onClause"])
        if whereClause is not None:
            statement += ' WHERE {}'.format(whereClause)
        return statement

    def createTable(self, model):
        self.cur.execute(self.createTableStatement(model))
        self.connection.commit()

    def dropTable(self, model):
        self.cur.execute(self.dropTableStatement(model))
        self.connection.commit()

    def insertRecords(self, model, records):
        if len(records) > 0:      
            for record in records:
                if len(record) != 0: # no field
                    try:
                        self.cur.execute(self.insertValuesStatement(model, record))
                    except:
                        print(sys.exc_info())
                        print("while inserting record to table", model["name"])
                        print("Record:",record)
                        return False
            self.connection.commit()

    def queryTable(self, fields, tableName, whereClause):
        self.cur.execute(self.queryTableStatement(fields, tableName, whereClause))
        rows = self.cur.fetchall()
        return rows

    def queryFromJoin(self, selectedFields, tableName, joinClauses, whereClause):
        self.cur.execute(self.queryFromJoinStatement(selectedFields, tableName, joinClauses, whereClause))
        rows = self.cur.fetchall()
        return rows
    
if __name__=="__main__":

    model = {
        "name" : "SprintIssueLink",
        "fields" : [
            {"name" : "sprintId", "type" : "TEXT" },
            {"name" : "issueId", "type" : "TEXT" }
        ],
        "primaryKeys" : [ "sprintId", "issueId" ]#,
        # "foreignKeys" : [
        #     {"name": "sprintId", "references": "Sprint(id)"},
        #     {"name": "issueId", "references": "Issue(id)"},
        # ]
    }

    connector = PostgresConnector()
    sprintIssueRecord = {'sprintId': 521, 'issueId': '36376'}
    sprintIssueRecords = [sprintIssueRecord]
    print(connector.insertValuesStatement(model, sprintIssueRecord))
    connector.insertRecords(model, sprintIssueRecords)
    

    # model_board = {
    # "name" : "Board",
    # "fields" : [
    #         { "name": "id", "type": "TEXT", "option" : "PRIMARY KEY" },
    #         { "name": "name" , "type": "TEXT"}
    #     ]
    # }
    # model_issueType = {
    # "name" : "IssueType",
    # "fields" : [
    #         { "name": "id", "type": "TEXT", "option" : "PRIMARY KEY" },
    #         { "name": "name" , "type": "TEXT"}
    #     ]
    # }
    # model_issue = {
    #     "name" : "Issue",
    #     "fields" : [
    #         {"name" : "id", "type" : "TEXT", "option" : "PRIMARY KEY" },
    #         {"name" : "name", "type" : "TEXT" },
    #         {"name" : "boardId", "type" : "TEXT" },
    #         {"name" : "issueTypeId", "type" : "TEXT" }
    #     ],
    #     "foreignKeys" : [
    #         {"name": "boardId", "references": "Board(id)"},
    #         {"name": "issueTypeId", "references": "IssueType(id)"}
    #     ]
    # }
    # connector = PostgresConnector()
    
    # connector.dropTable(model_issue)
    # connector.dropTable(model_issueType)
    # connector.dropTable(model_board)
    # connector.createTable(model_board)
    # connector.createTable(model_issueType)
    # connector.createTable(model_issue)

    # # board
    # board_data = [{'id':'board#1', 'name':'board#1'},\
    #                  {'id':'board#2', 'name':'board#2'},\
    #                  {'id':'board#3', 'name':'board#3'}]
    # connector.insertRecords(model_board, board_data)

    # # issueType
    # issueType_data = [{'id':'issueType#1', 'name':'issueType#1'},\
    #                 {'id':'issueType#2', 'name':'issueType#2'},\
    #                 {'id':'issueType#3', 'name':'issueType#3'}]
    # connector.insertRecords(model_issueType, issueType_data)

    # # issue
    # issue_data = [{'id':'issue#1', 'name':'issue#1', 'boardId':'board#1', 'issueTypeId':'issueType#1'},\
    #                 {'id':'issue#2', 'name':'issue#2', 'boardId':'board#2', 'issueTypeId':'issueType#2'},\
    #                 {'id':'issue#3', 'name':'issue#3', 'boardId':'board#3', 'issueTypeId':None}]
    # connector.insertRecords(model_issue, issue_data)
    
    # # query
    # whereClause = "Issue.id != 'issue#1'" # use single quote inside of clause since Postgres doesn't allow double quotes
    # print(connector.queryTable(['name'], 'Issue', whereClause))

    # statement = connector.queryTableStatement(['name'], 'Issue', whereClause)

    # print(pd.read_sql_query(statement, connector.connection))

    # # join table query
    # joinClauses = [
    #     {"type":"LEFT", "tableName":"IssueType", "onClause":"Issue.issueTypeId = IssueType.id"},
    #     {"type":"LEFT", "tableName":"Board", "onClause":"Issue.boardId = Board.id"}
    # ]
    # statement = connector.queryFromJoinStatement(['Issue.name as issue', 'Board.name as board', 'IssueType.name as type'], 'Issue', joinClauses, whereClause)
    # print(pd.read_sql_query(statement, connector.connection))



    