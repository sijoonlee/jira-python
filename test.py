from businessLogic.db.dbActions import DbActions
from db.redshift.connector import RedshiftConnector
from jira.jiraRequests.responseProcessor import responseProcessor
'''
https://docs.aws.amazon.com/redshift/latest/dg/merge-examples.html
-- Create a staging table and populate it with updated rows from SALES_UPDATE 

create temp table stageboard as
select * from board
where id = {boardId}

-- Start a new transaction
begin transaction;

delete from board
using stageboard
where board.id = stageboard.id

-- Insert all the rows from the staging table into the target table
insert into sales
select * from stagesales;

-- End transaction and commit
end transaction;

-- Drop the staging table
drop table stagesales;
'''

if __name__=="__main__":
    # dbActions = DbActions(RedshiftConnector, responseProcessor, maxWorkers=4)
    # dbActions.reset()
    model = {
        "name" : "Board",
        "fields" : [
            { "name": "id", "type": "TEXT", "option" : "PRIMARY KEY" },
            { "name": "name" , "type": "TEXT"},
            { "name": "type", "type": "TEXT"},
            { "name": "projectId", "type": "TEXT"}
        ]
    }
    model = {
        "name" : "SprintIssueLink",
        "fields" : [
            {"name" : "sprintId", "type" : "TEXT" },
            {"name" : "issueId", "type" : "TEXT" }
        ],
        "primaryKeys" : [ "sprintId", "issueId" ]
    }
    # record = {'id':'test#1', 'name':'board#1', 'type':'type#1', 'projectId':'project#1'}
    # records = [ {'id':'test#1', 'name':'board#1', 'type':'type#1', 'projectId':'project#1'} ]
    records = [{'sprintId':'s#1', 'issueId':'i#1'}]
    connector = RedshiftConnector()
    connector.insertRecords(model, records)

    # print(connector.insertValuesStatement(model, record))
    # connector.insertRecords(model,records )

    # query = '''
    #     begin transaction;
    #     delete from {table} where {pkField} = {pkValue};
    #     insert into {table}({fields}) values({values});
    #     end transaction;
    #     '''.format(table='board', pkField='id', pkValue="'id#3'", fields='id, name, type', values="'id#3', 'test', 'test'")

    # print(query)    
    # connector.runQueryStatement(query)
    
    print(connector.queryTable(["*"],'SprintIssueLink',None))