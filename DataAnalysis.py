# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 12:53:43 2015

@author: alexsutherland
"""

import sqlalchemy 
import pandas as pd
import sklearn as skl
import matplotlib.pyplot as plt

def loadData():
    
    columnsToLoad = 'Gender,Age,Height,startWeight, \
                    endWeight,weightChange,TimeElapsedEpoch,\
                    postEpochTime, username,title'
    
    sqlEngine = sqlalchemy.create_engine('mysql+pymysql://root@localhost/RedditWeightDatabase')
    con = sqlEngine.connect()
    sqlResult = con.execute("SELECT "+columnsToLoad+" FROM redditWeightTable")
    
    df = pd.DataFrame(sqlResult.fetchall())
    df.columns = sqlResult.keys()
    
    return df

fullData = loadData()



plt.scatter(fullData['Age'], fullData['weightChange'], 'ro')
