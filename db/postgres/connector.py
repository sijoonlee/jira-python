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
        print("DB connection established")
    
    def __del__(self):
        print("DB connection closed")
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
                elif fieldType is "TIMESTAMPTZ" or fieldType is "TIMESTAMP":
                    fieldValues[i] = "'{}'".format(fieldValues[i])
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
        else : # there's no fields other than PK, which means there's nothing to update in case of PK conflict
            statement += ' on conflict do nothing'
    
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
