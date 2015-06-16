# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 10:56:14 2015

@author: alexsutherland
"""

import urllib2
import redditScrapingTools as rst
import pandas as pd
import json
import time
import redditDataIO as dataIO


#fullData = dataIO.loadData()

userList = fullData['username'].unique()

#When restarting
'''
lastUsername = 'HansChuzzman'
lastUsernameIndex = pd.DataFrame(userList)[pd.DataFrame(userList)[0] == lastUsername]
'''

#def scrapeUserInfo(userList):

userIdArray = {}

scrapedSuccesses = []
userData = [] 

fullUserCommentData = []
userID = 1
for index, username in enumerate(userList):
    print str(index) + ' out of ' + str(len(userList)) + ' users scraped'
    newUser = True
    currentUserCommentData = []
    requestURL = 'https://www.reddit.com/user/' + username + '/comments/.json?limit=100'

    print requestURL
    
    hasNextButton = True
    scrapedAttempts = 0
    currentSuccesses = 0
    while hasNextButton:
        
        #Generates reddit request and gets full HTML of the user's comment page
        req = urllib2.Request(requestURL)
        req.add_header('User-Agent', 'Python:Insight ProgressPic Weight Prediction (by /u/gahathat)')
        try:        
            page = urllib2.urlopen(req)
        except:
            break
        pageJSON = json.loads(page.read())        
        
        scrapedAttempts += 100    #Each page has 25 posts
        print str(scrapedAttempts) + ' scrapes'
        #Get the HTML for each post
        for comment in pageJSON['data']['children']:
            commentData = pd.Series(comment['data'])
            currentData = commentData[['score','controversiality','body','subreddit','link_title','link_id','created_utc']]
            currentData['username'] = username
            
            #If the username already exists
            if username in userIdArray.keys():
                currentData['userid'] = userIdArray[username]
                newUser = False
            else:
                userIdArray[username] = userID
                currentData['userid'] = userID
                userID += 1
                
                
            currentUserCommentData.append(currentData)
        #For the final comment Data, get the next URL
            
        
        #Generate the next page's URL
        nextCode = str(pageJSON['data']['after'])
        if nextCode == 'None':
            hasNextButton = False
            break
        else:
            requestURL = 'https://www.reddit.com/user/' + username + '/comments/.json?count='+ str(scrapedAttempts) + '&after=' + nextCode

        
        #Pause to throttle scraping rate
        time.sleep(1.5)
    #End while hasNextButton
    fullUserCommentData.extend(currentUserCommentData)
        
    #Append the current timestamp and the fraction of scraping successes
    #scrapedSuccesses.append([currentSuccesses/float(scrapedAttempts)])

fullUserCommentData = pd.DataFrame(fullUserCommentData)

#return fullUserCommentData