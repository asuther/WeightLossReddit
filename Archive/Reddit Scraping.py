
# coding: utf-8

# #Scraping r/ProgressPics titles and usernames

# In[1]:

get_ipython().magic(u'matplotlib inline')

import time
import numpy as np
import sys
sys.path.append('/Users/alexsutherland/Dropbox/Programming/Python/Insight')
import redditScrapingTools as rst
import pandas as pd


# Next, we run through all months between June 1st 2013, and June 1st, 2015 (in reverse order).
# 
# Lots of user information is scraped from this: 'Gender','Age','Height','startWeight','endWeight','weightChange','TimeElapsed','TimeUnit','userText','username','title','commentCount','votes','postDateTime'

# In[2]:

scrapedSuccesses = []            #ScrapedSuccesses will store the time period and the fraction of successful scrapes
data = []                        #data will store the scraped data
timeStampJune2011 = 1306919308
timeStampMar2013 = 1364458036
timeStampJune2015 = 1433317589  #This is June 1st, 2015
timeStampJune2013 = 1370072789  #June 1st, 2013
monthTime = 2592000             #This is the approximate timespan of a month in seconds
dayTime = int(2592000 / (7*30))


# In[42]:

startTime = timeStampJune2011
endTime = timeStampJune2015

for timestampStart in np.arange(timeStampJune2011 + (6*monthTime), endTime, monthTime):

    fullHTML = rst.getHTMLData(timestampStart)

    hasNextButton = True
    scrapedAttempts = 0
    currentSuccesses = 0
    while hasNextButton:
        scrapedAttempts += 25    #Each page has 25 posts
        print str(scrapedAttempts) + ' scrapes'
        #Get the HTML for each post
        rawPostHTMLArray = fullHTML.findAll('div',{'onclick':'click_thing(this)'})
        
        #For each post
        for index, rawPost in enumerate(rawPostHTMLArray):
            #Get the data associated with it
            postData = rst.getPostData(rawPost)
            if not postData == -1:
                data.append(postData)
                currentSuccesses+=1
                #print currentSuccesses
        #End for all raw posts
        
        #Generate the next page's URL
        fullHTML = rst.getNextPageHTML(fullHTML)

        #If the page has no results
        if fullHTML.find('span', {'class':'nextprev'}) is None:
            break 
        
        
        #Check to see if the next page has a next button

        snoopedNextHref = fullHTML.find('span', {'class':'nextprev'}).find('a',{'rel':'nofollow next'})
        #If the next page does not have a next button, stop the current while loop and move onto the next time range
        if snoopedNextHref is None:
            hasNextButton = False
        
        #Pause to throttle scraping rate
        time.sleep(2)
    #End while hasNextButton
    
    #Append the current timestamp and the fraction of scraping successes
    scrapedSuccesses.append([timestampStart, currentSuccesses/float(scrapedAttempts)])




# ##Weight Loss Result Data
# The column names are set and the data is converted into a dataframe

# In[4]:

columnNames = ['gender','age','height','startWeight','endWeight','weightChange','weightUnit',
              'timeElapsed','timeUnit','userText','username','title','commentCount',
              'votes','postDateTime','postURL','postId']

fullData = pd.DataFrame(data, columns=columnNames)
print fullData