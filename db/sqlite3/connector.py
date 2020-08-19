import os
import sqlite3

class SqliteConnector(object):
    def __init__(self, dbFilePath):
        # path = os.path.dirname(os.path.abspath(__file__))
        # dbFile = path + '/db/sqlite3/storage/db.sqlite'
        if not os.path.exists(dbFilePath):
            print("File does not exist: ", dbFilePath)
            os.mknod(dbFilePath)
            print("New file created")
        self.connection = sqlite3.connect(dbFilePath)
        self.cur = self.connection.cursor()
    
    def __del__(self):
        self.connection.close()
        
    def dropTableStatement(self, model):
        return 'DROP TABLE IF EXISTS {tableName}'.format(tableName = model["name"])

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
            statement += ',PRIMARY KEY ('
            for i in range(len(primaryKeys)):
                statement += primaryKeys[i]
                if i < len(primaryKeys) - 1 :
                    statement += ','
            statement += ")"

        foreignKeys = model.get("foreignKeys", None)
        if foreignKeys is not None:
            statement += ','
            for i in range(len(foreignKeys)):
                statement += "FOREIGN KEY ({name}) REFERENCES {references}" \
                    .format(name=foreignKeys[i]["name"],references=foreignKeys[i]["references"])
                if i < len(foreignKeys) - 1 :
                    statement += ','
        statement += ")"
        
        return statement

    def findTypeFromFieldName(self, model, fieldName):
        fieldType = None
        for field in model["fields"]:
            if field["name"] is fieldName:
                fieldType = field["type"]
                break
        return fieldType


    # @param : fields 
    # key is field name, value is the value for the field
    # { "accountId" : "USER_ID", "accountType" : "USER_TYPE" }
    def insertValuesStatement(self, model, fields):
        
        fieldNames = list(fields.keys())
        fieldValues = list(fields.values())

        for i in range(len(fieldNames)):
            fieldType = self.findTypeFromFieldName(model, fieldNames[i])
            if fieldType is "INTEGER" or fieldType is "REAL" or fieldType is "NULL":
                fieldValues[i] = str(fieldValues[i])
            elif fieldType is "TEXT" or fieldType is "BLOB":
                 # single, double quotes, new line, carriage return are escaped
                 # in sqlite you can escape by using ""(two double quotes) , ''(two sing quotes)
                escaped = str(fieldValues[i]).replace('"', '""').replace("'", "\'\'") #.replace('\n', ' ').replace('\r', '')
                fieldValues[i] = '"{}"'.format(escaped)
            else:
                print("Error - Unknown type: ", fieldType)

        fieldNames = ','.join(fieldNames)
        fieldValues = ','.join(fieldValues)
        statement = 'insert or replace into {table} ({fieldNames}) values ({fieldValues})'.format(table=model["name"], fieldNames=fieldNames, fieldValues=fieldValues)
        return statement


    # @param: selectedFields - list of fields that are to be returned ex) ["id", "name", "creator"]
    # @param: whereClause - dictionary of fields that will be used in where clause 
    def queryTableStatement(self, selectedFieldNames, tableName, whereClause):
        
        if len(selectedFieldNames) > 1:
            selectedFieldNames = ",".join(selectedFieldNames)
        elif len(selectedFieldNames) == 1:
            selectedFieldNames = selectedFieldNames[0]

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

    def insertOneRecord(self, model, record):
        if len(record) != 0: # no field
            self.cur.execute(self.insertValuesStatement(model, record))
            self.connection.commit()

    def insertRecords(self, model, records):
        if len(records) != 0:
            for record in records:
                if len(record) != 0: # no field
                    self.cur.execute(self.insertValuesStatement(model, record))
            self.connection.commit()

    def queryTable(self, fields, tableName, whereClause):
        self.cur.execute(self.queryTableStatement(fields, tableName, whereClause))
        rows = self.cur.fetchall()
        return rows

    def queryFromJoin(self, selectedFields, tableName, joinClauses, whereClause):
        self.cur.execute(self.queryFromJoinStatement(selectedFields, tableName, joinClauses, whereClause))
        rows = self.cur.fetchall()
        return rows
    
    