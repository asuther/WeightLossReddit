# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 21:13:36 2015

@author: alexsutherland
"""

import re
from BeautifulSoup import BeautifulSoup
import urllib2
import time
import numpy as np
import redditScrapingTools as rst

#baseURL = 'http://www.reddit.com/r/progresspics/?sort=top&t=all&syntax=cloudsearch&q=timestamp%3A'
baseURL = 'https://www.reddit.com/r/progresspics/search?restrict_sr=on&sort=relevance&t=all&syntax=cloudsearch&q=%28and+title:%27%27%29+timestamp:'
timeStampJune2013 = 1370072789
timeStampJune2015 = 1433317589
monthTime = 2592000

scrapedSuccesses = []
data = []

for timestampStart in np.arange(timeStampJune2013, timeStampJune2015, monthTime):
    
    fullHTML = rst.getHTMLData(timestampStart)  
    
    hasNextButton = True
    scrapedAttempts = 0
    currentSuccesses = 0
    while hasNextButton:
        rawPostArray = fullHTML.findAll('div',{'onclick':'click_thing(this)'})
        
        patternString = '(M|F)\/(\d+)\/(\d+)[\'|,|\’](\d+)*(?:\"|\'\'|\s|&quot;|\”)*.*\[(\d+)[^\d]+(\d+)(?:.*\=[^\d]*(\d+).*)*.*\].*(?:\[|\()[^\d]*(\d+)[.]*(\d+)*\s*(months|weeks|mo|month|week|year|years|days)*.*(?:\)|\])(.*)'
        
        scrapedAttempts += 25
        for index, rawPost in enumerate(rawPostArray):
            
            titleData = rawPost.find("a", {"class": "title may-blank "})
            
            #Get Username        
            usernameTemp = rawPost.find('a',{'class':re.compile(r"author.*")})
            if not usernameTemp is None:
                username = str(usernameTemp.contents[0])
            else:
                username = ''
            
            commentArray = str(rawPost.find('a',{'class':re.compile(r"comments.*")}).contents[0]).split(' ')
            if len(commentArray) == 2:
                commentCount = int(commentArray[0])
            else:
                commentCount = 0
            
            votes = rawPost.find('div',{'class':'score unvoted'}).contents[0]
            if votes == '&bull;':
                votes = 0
            else:
                votes = int(votes)
    
            postDateTime = str(rawPost.find('time').get('datetime'))
            print postDateTime            
            
            currentData = {}
            #try:
            title = str(titleData.contents[0])
            title = title.replace("”",'"')
            title = title.replace("’","'")
            #except:
            #    title = unicodedata.normalize('NFKD', title.contents[0]).encode('ascii','ignore')
    
            patternFinder = re.compile(patternString, re.IGNORECASE)
            titleMatches = patternFinder.match(title)
            
            if not titleMatches is None:
                #print index
                #print title
                currentData['Gender'] = titleMatches.group(1)
                currentData['Age'] = titleMatches.group(2)
                #If there is both height in feet and inches
                if not titleMatches.group(4) is None:
                    currentData['Height'] = (int(titleMatches.group(3))*12) + int(titleMatches.group(4))
                #Else, there's only height in feet
                else:
                    currentData['Height'] = int(titleMatches.group(3))*12
    
                currentData['startWeight'] = int(titleMatches.group(5))
                currentData['endWeight'] = int(titleMatches.group(6))
                if not titleMatches.group(7) is None:
                    currentData['weightChange'] = int(titleMatches.group(7))
                else:
                    currentData['weightChange'] = currentData['endWeight'] - currentData['startWeight']
                currentData['TimeElapsed'] = int(titleMatches.group(8))
                currentData['TimeUnit'] = titleMatches.group(10)
                currentData['userText'] = titleMatches.group(11)
                currentData['username'] = username
                currentData['title'] = title
                currentData['commentCount'] = commentCount
                currentData['votes'] = votes
                currentData['postDateTime'] = postDateTime
                
                data.append(currentData)
                currentSuccesses+=1
            else:
                #print title
                pass
    
        
        nextHref = fullHTML.find('span', {'class':'nextprev'}).find('a',{'rel':'nofollow next'}).get('href')
        
        req = urllib2.Request(nextHref)
        req.add_header('User-Agent', 'Python:Insight ProgressPic Weight Prediction (by /u/gahathat)')
        page = urllib2.urlopen(req)   
        fullHTML = BeautifulSoup(page.read())
        snoopedNextHref = fullHTML.find('span', {'class':'nextprev'}).find('a',{'rel':'nofollow next'})
        if snoopedNextHref is None:
            hasNextButton = False
    
        
        #Pause to throttle scraping rate
        time.sleep(2.5)
    
    scrapedSuccesses.append([timestampEnd, currentSuccesses/float(scrapedAttempts)])

columnNames = ['Gender','Age','Height','startWeight','endWeight','weightChange',
              'TimeElapsed','TimeUnit','userText','username','title','commentCount',
              'votes','postDateTime']