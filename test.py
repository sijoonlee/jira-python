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
    sss = "abcdef"
    sss
    print(len(sss[:10]))