
import pymysql as mdb
import sqlalchemy 
import pandas as pd

def exportDataToSQL(data, tableName='redditWeightTable'):

    print data.columns
    con = mdb.connect('localhost', 'root', '', 'RedditWeightDatabase') #host, user, password, #database
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS " + tableName)
    
    
    sqlEngine = sqlalchemy.create_engine('mysql+pymysql://root@localhost/RedditWeightDatabase')
    
    data.to_sql(tableName, sqlEngine)
    
    print 'Exported Data to SQL Table (Name: ' + tableName + ')'


def loadData(tableName = 'redditWeightTable'):
    
    sqlEngine = sqlalchemy.create_engine('mysql+pymysql://root@localhost/RedditWeightDatabase')
    con = sqlEngine.connect()
    sqlResult = con.execute("SELECT * FROM " + tableName)
    
    df = pd.DataFrame(sqlResult.fetchall())
    df.columns = sqlResult.keys()

    
    return df