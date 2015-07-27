
import pymysql as mdb
import sqlalchemy 
import pandas as pd

def exportDataToSQL(dataFrame, tableName='defaultName'):

    hostName = 'localhost'    
    userName = 'root'
    pw = ''
    databaseName = 'test'
    
    #Connect to the database
    con = mdb.connect(hostName, userName, pw, databaseName)
    cur = con.cursor()
    
    #Deletes the old version of the table
    cur.execute("DROP TABLE IF EXISTS " + tableName)
    
    #Connect to database via sql alchemy
    sqlEngineString = 'mysql+pymysql://{1}:{2}@{0}/{3}'.format(hostName, userName, pw, databaseName)
    sqlEngine = sqlalchemy.create_engine(sqlEngineString)
    
    #Export the full dataframe to the sql database
    dataFrame.to_sql(tableName, sqlEngine)
    
    print 'Exported Data to SQL Table (Name: ' + tableName + ')'