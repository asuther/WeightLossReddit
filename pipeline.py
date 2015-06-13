# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 13:06:57 2015

@author: alexsutherland
"""

import DataCleaning
import FeatureAdditions
import DataExporting
import redditScraping
#import userScraping

def runScrapePipeline():
    
    data = redditScraping.scrapeData()
    
    cleanedData = cleanExportPipeline(data)
    
    userScraping.scrapeUserInfo(cleanedData['username'].unique())
    
    return cleanedData

def cleanExportPipeline(data):
    cleanedData = DataCleaning.cleanData(data)
    
    featureCleanedData = FeatureAdditions.addFeatures(cleanedData)

    DataExporting.exportDataToSQL(featureCleanedData)
    
    return featureCleanedData
'''
def getUserInformation(data):
    uniqueUserList = data['username'].unique()
    
    userScraping.scrapeUserKarma(uniqueUserList)
   ''' 
  
#cleanExportPipeline(fullData)