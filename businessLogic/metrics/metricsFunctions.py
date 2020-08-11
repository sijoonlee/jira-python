import pandas as pd

# @param: connection - db connection object
# @param: queryStatement - sql query statement
# @param: groupField - field that is used as group
def countByGroup(connection, queryStatement, groupField):
    df = pd.read_sql_query(queryStatement, connection)
    df['Count'] = ""
    grouped = df.groupby(groupField).count()
    return grouped

def percentageByGroup(connection, queryStatement, groupField):
    grouped = countByGroup(connection, queryStatement, groupField)
    grouped['Percentage'] = grouped['Count']/grouped['Count'].sum()
    return grouped
