
import pymysql as mdb
import sqlalchemy 
import pandas as pd

def exportDataToSQL(data):

    print data.columns
    con = mdb.connect('localhost', 'root', '', 'RedditWeightDatabase') #host, user, password, #database
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS redditWeightTable")
    
    
    sqlEngine = sqlalchemy.create_engine('mysql+pymysql://root@localhost/RedditWeightDatabase')
    
    data.to_sql('redditWeightTable', sqlEngine)
    
    print 'Exported Data to SQL Table'


def loadData():
    
    sqlEngine = sqlalchemy.create_engine('mysql+pymysql://root@localhost/RedditWeightDatabase')
    con = sqlEngine.connect()
    sqlResult = con.execute("SELECT * FROM redditWeightTable")
    
    df = pd.DataFrame(sqlResult.fetchall())
    df.columns = sqlResult.keys()
    
    return df