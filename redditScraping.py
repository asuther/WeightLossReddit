
# coding: utf-8

# #Scraping r/ProgressPics titles and usernames

import time
import numpy as np
import sys
sys.path.append('/Users/alexsutherland/Dropbox/Programming/Python/Insight')
import redditScrapingTools as rst
import pandas as pd


# Next, we run through all months between June 1st 2013, and June 1st, 2015 (in reverse order).
# 
# Lots of user information is scraped from this: 'Gender','Age','Height','startWeight','endWeight','weightChange','TimeElapsed','TimeUnit','userText','username','title','commentCount','votes','postDateTime'

def scrapeData():
    scrapedSuccesses = []            #ScrapedSuccesses will store the time period and the fraction of successful scrapes
    data = []                        #data will store the scraped data
    timeStampJune2011 = 1306919308
    timeStampMar2013 = 1364458036
    timeStampJune2015 = 1434405307  #This is June 1st, 2015
    timeStampJune2013 = 1370072789  #June 1st, 2013
    monthTime = 2592000             #This is the approximate timespan of a month in seconds
    dayTime = int(2592000 / (7*30))
    
    startTime = timeStampJune2011
    endTime = timeStampJune2015
    
    for timestampStart in np.arange(timeStampJune2011, timeStampJune2015, monthTime):
    
        fullJSON, fullURL = rst.getJSONData(timestampStart)
    
        hasNextButton = True
        scrapedAttempts = 0
        currentSuccesses = 0
        while hasNextButton:
            scrapedAttempts += 100    #Each page has 25 posts
            print str(scrapedAttempts) + ' scrapes'
             
            #For each post
            for rawPost in fullJSON['data']['children']:
                #Get the data associated with it
                postData = rst.getPostData(pd.Series(rawPost['data']))
                if not postData == -1:
                    data.append(postData)
                    currentSuccesses+=1
                    #print currentSuccesses
            #End for all raw posts
    
    
            #Pause to throttle scraping rate
            time.sleep(1.5)
            
            #If the page has no results
            nextCode = str(fullJSON['data']['after'])
            print nextCode
            if nextCode in ['None','null']:
                hasNextButton = False
                break
            else:
                fullJSON = rst.getNextPageJSON(nextCode, fullURL, scrapedAttempts)
            
            
            
        #End while hasNextButton
        
        #Append the current timestamp and the fraction of scraping successes
        scrapedSuccesses.append([timestampStart, currentSuccesses/float(scrapedAttempts)])
    
    # ##Weight Loss Result Data
    # The column names are set and the data is converted into a dataframe
    
    fullData = pd.DataFrame(data, columns=data[0].keys())
    return fullData