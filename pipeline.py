# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 13:06:57 2015

@author: alexsutherland
"""

import DataCleaning
import FeatureAdditions
import redditDataIO
import redditScraping
#import userScraping
import time

def runScrapePipeline():
    
    data = redditScraping.scrapeData()
    
    #cleanedData = cleanExportPipeline(data)
    
    featureCleanedData = FeatureAdditions.addFeatures(data)

    redditDataIO.exportDataToSQL(featureCleanedData)
    
    #userScraping.scrapeUserInfo(cleanedData['username'].unique())
    
    return featureCleanedData

def cleanExportPipeline(data):
    cleanedData = DataCleaning.cleanData(data)
    
    featureCleanedData = FeatureAdditions.addFeatures(cleanedData)

    redditDataIO.exportDataToSQL(featureCleanedData)
    
    return featureCleanedData
'''
def getUserInformation(data):
    uniqueUserList = data['username'].unique()
    
    userScraping.scrapeUserKarma(uniqueUserList)
   ''' 

startTime = time.time()
fullData = runScrapePipeline()
endTime = time.time()