import sqlite3

# This function simply converts a single column of a database table into a
# list of values.
def convertColumnToList(connection,columnName, tableName):
    c = connection.cursor()

    executeString = 'SELECT "' + columnName + '" FROM ' + tableName
    c.execute(executeString)

    dataArray = c.fetchall()

    returnArray = []
    for row in dataArray:
        returnArray.append(row[0])

    return returnArray
