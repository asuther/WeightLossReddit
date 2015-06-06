
import pymysql as mdb
import sqlalchemy 

def exportDataToSQL(data):

    con = mdb.connect('localhost', 'root', '', 'RedditWeightDatabase') #host, user, password, #database
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS redditWeightTable")
    
    
    sqlEngine = sqlalchemy.create_engine('mysql+pymysql://root@localhost/RedditWeightDatabase')
    
    data.to_sql('redditWeightTable', sqlEngine)

