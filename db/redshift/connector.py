import psycopg2
import os
import sys
import pandas as pd
from config import config

class RedshiftConnector(object):
    def __init__(self):
        self.connection = psycopg2.connect(dbname=config["redshiftDbName"],
                                            host=config["redshiftHost"], 
                                            port=config["redshiftPort"], 
                                            user=config["redshiftUser"], 
                                            password=config["redshiftPassword"])
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
        primaryKeys = set() # set to avoid duplicates

        if model.get('primaryKeys', None) != None:
            primaryKeys = {*model['primaryKeys']}
            
        if model.get("fields", None) != None:
            fields = model["fields"]
            for field in fields:
                if field.get("option", None) == 'PRIMARY KEY':
                    primaryKeys.add(field["name"])
                    
        return list(primaryKeys) # array


    # @param : model
    # this is schema for a table in database
    #   model = {
    #     "name" : "Board",
    #     "fields" : [
    #         { "name": "id", "type": "TEXT", "option" : "PRIMARY KEY" },
    #         { "name": "name" , "type": "TEXT"},
    #         { "name": "type", "type": "TEXT"},
    #         { "name": "projectId", "type": "TEXT"}
    #     ]
    #   }
    # @param : record
    # key is field name, value is the value for the field
    #   { "id":"id#1", "name":"board#1", "type":"type#1", "projectId":"project#1" }
    # @return : string 
    # SQL statment that has delete/insert statement to avoid duplication
    # Because redshift doesn't check ducplicates for primary key, 
    # it is needed to delete the existing record first
    # (multiple records with the same PK can happen in Redshift)
    #   begin transaction;
    #   delete from Board where id = 'id#1';
    #   insert into Board (id,name,type,projectId) values ('id#1','board#1','type#1','project#1');
    #   end transaction;
    def insertValuesStatement(self, model, record):
        
        fieldNames = list(record.keys())
        fieldToBeDeleted = []
        
        for fieldName in fieldNames:
            fieldType = self.findTypeFromFieldName(model, fieldName)
            if record[fieldName] != None:
                if fieldType == "INTEGER" or fieldType == "REAL" or fieldType == "BOOLEAN":
                    record[fieldName] = str(record[fieldName])
                elif fieldType == "TEXT":
                    # single, double quotes are escaped
                    # in sqlite you can escape by using ""(two double quotes) , ''(two sing quotes)
                    escaped = str(record[fieldName]).replace("'", "''").replace('"', '""') #.replace('\n', ' ').replace('\r', '')
                    record[fieldName] = "'{}'".format(escaped[:256]) # limit of 256 characters
                else:
                    print("Error - Unknown type: ", fieldType)
            else:
                # This is to delete the field when the value is null
                fieldToBeDeleted.append(fieldName) 

        # Delete fields with null value, Database can use default value or null value depending on its setting
        for field in fieldToBeDeleted:
            record.pop(field)

        primaryKeys = self.findPrimaryKey(model)

        # delete statement
        primaryValues = [record[key] for key in primaryKeys]
        primaryKeyValues = tuple(zip(primaryKeys, primaryValues))
        whereClausePK = ["{} = {}".format(pair[0], pair[1]) for pair in primaryKeyValues]
        whereClausePK = " AND ".join(whereClausePK)
        deleteStatement = 'delete from {table} where {whereClausePK};'\
            .format(table=model["name"], whereClausePK=whereClausePK)

        # insert statement
        primaryKeys = ','.join(primaryKeys)
        fieldNames = list(record.keys())
        fieldValues = list(record.values())
        fieldNames = ','.join(fieldNames)
        fieldValues = ','.join(fieldValues)

        insertStatement = 'insert into {table} ({fieldNames}) values ({fieldValues});'\
            .format(table=model["name"], fieldNames=fieldNames, fieldValues=fieldValues)
            
        statement = '''
            {deleteStatement}
            {insertStatement}
            '''.format(deleteStatement=deleteStatement, insertStatement=insertStatement)

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
            #self.cur.execute('begin transaction;')      
            for record in records:
                if len(record) != 0: # no field
                    try:
                        self.cur.execute(self.insertValuesStatement(model, record))
                    except:
                        print(sys.exc_info())
                        print("while inserting record to table", model["name"])
                        print("Record:",record)
                        return False
            #self.cur.execute('end transaction;')
            self.connection.commit()

    def queryTable(self, fields, tableName, whereClause):
        self.cur.execute(self.queryTableStatement(fields, tableName, whereClause))
        rows = self.cur.fetchall()
        return rows

    def queryFromJoin(self, selectedFields, tableName, joinClauses, whereClause):
        self.cur.execute(self.queryFromJoinStatement(selectedFields, tableName, joinClauses, whereClause))
        rows = self.cur.fetchall()
        return rows

    def runQueryStatement(self, query):
        self.cur.execute(query)
        self.connection.commit()
