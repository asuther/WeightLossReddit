# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 13:04:40 2015

@author: alexsutherland
"""

import urllib2
from BeautifulSoup import BeautifulSoup
import re
import titleParsingTools as tpt

baseURL = 'https://www.reddit.com/r/progresspics/search?restrict_sr=on&sort=relevance&limit=100&t=all&syntax=cloudsearch&q=%28and+title:%27%27%29+timestamp:'

#TimeStamp Info
timeStampJune2015 = 1433317589  #This is June 1st, 2015
timeStampJune2013 = 1370072789  #June 1st, 2013
monthTime = 2592000             #This is the approximate timespan of a month in seconds
postTitlePatternString = '(M|F|male|female)\s?\/\s?(\d+)\s?\/\s?(\d+)(?:\'|,|\’|foot)\s?(\d+)*(?:\"|\'\'|\s|inches|&quot;|\”)*.*(?:\[|\()(\d+)[\s]?(kg|lb)?[^\d]+(\d+)[\s]?(kg|lb|lbs)?(?:[^\d]*\=[^\d]*(\d+)[\s]?(kg|lb|lbs)?.*)?(?:\]|\))\s?(?:\[|\(|\s)[^\d]*(\d+)[.]?(\d+)?\s?(months|weeks|mo|month|week|year|years|days)?\s?(?:\)|\]|\s)\s?(.*)'

def getHTMLData(timestampStart):
    
    timestampRange = str(timestampStart) + '..' + str(timestampStart + monthTime)   #Creates a string of the time range
    
    print baseURL + timestampRange
    #Generates reddit request and gets full HTML of the search page
    req = urllib2.Request(baseURL+timestampRange)
    req.add_header('User-Agent', 'Python:Insight ProgressPic Weight Prediction (by /u/gahathat)')
    page = urllib2.urlopen(req)
    fullHTML = BeautifulSoup(page.read())
    
    return fullHTML
    
def getPostTextInfo(postHTML):
    
    postTextData = {}
    
    #Get Username        
    usernameTemp = postHTML.find('a',{'class':re.compile(r"author.*")})
    if not usernameTemp is None:
        postTextData['username'] = str(usernameTemp.contents[0])
    else:
        postTextData['username'] = ''
    
    commentArray = str(postHTML.find('a',{'class':re.compile(r"comments.*")}).contents[0]).split(' ')
    if len(commentArray) == 2:
        postTextData['commentCount'] = int(commentArray[0])
    else:
        postTextData['commentCount'] = 0
    
    votes = postHTML.find('div',{'class':'score unvoted'}).contents[0]
    if votes == '&bull;':
        postTextData['votes'] = 0
    else:
        postTextData['votes'] = int(votes)
    
    postTextData['postDateTime'] = str(postHTML.find('time').get('datetime'))
    
    postTextData['postURL'] = postHTML.find('a',{'class':re.compile(r"title.*")}).get('href')
    
    postTextData['postId'] =str(postHTML.get('data-fullname'))
    
    return postTextData

def getPostTitle(postHTML):
    titleHTML = postHTML.find("a", {"class": "title may-blank "})
    
    title = str(titleHTML.contents[0])
    title = title.replace("”",'"')
    title = title.replace("’","'")
    
    return title

def getPostTitleData(postTitle):
    titleData = {}
    
        
    patternFinder = re.compile(postTitlePatternString, re.IGNORECASE)
    titleMatches = patternFinder.match(postTitle)
        
    #If title matches has info
    if not titleMatches is None:
        #print index
        #print title
        titleData['Gender'] = str(titleMatches.group(1)).upper()
        titleData['Age'] = int(titleMatches.group(2))
        #If there is both height in feet and inches
        if not titleMatches.group(4) is None:
            titleData['Height'] = (int(titleMatches.group(3))*12) + int(titleMatches.group(4))
        #Else, there's only height in feet
        else:
            titleData['Height'] = int(titleMatches.group(3))*12
    
        titleData['startWeight'] = int(titleMatches.group(5))
    
        firstWeightUnit = titleMatches.group(6) or ''
        
        titleData['endWeight'] = int(titleMatches.group(7))
       
        secondWeightUnit = titleMatches.group(8) or ''
        
        if not titleMatches.group(9) is None:
            titleData['weightChange'] = int(titleMatches.group(9))
        else:
            titleData['weightChange'] = int(titleData['startWeight'] - titleData['endWeight'])

        thirdWeightUnit = titleMatches.group(10) or ''
        
        if len(firstWeightUnit) > 0:
            titleData['weightUnit'] = firstWeightUnit.lower()
        elif len(secondWeightUnit) > 0:
            titleData['weightUnit'] = secondWeightUnit.lower()
        elif len(thirdWeightUnit) > 0:
            titleData['weightUnit'] = thirdWeightUnit.lower()
        else:
            titleData['weightUnit'] = ''
        
        titleData['TimeElapsed'] = int(titleMatches.group(11))
        if not titleMatches.group(12) is None:
            stringNumber = str(titleMatches.group(11)) + '.' + str(titleMatches.group(12))
            titleData['TimeElapsed'] = float(stringNumber)
        
        titleData['TimeUnit'] = titleMatches.group(13)
        titleData['userText'] = titleMatches.group(14)

              
        
        titleData['title'] = postTitle
            
    return titleData
    
def getPostTitleManual(postTitle):    
    bodyInfoPattern = '(M|F|male|female)\s?\/\s?(\d+)\s?\/\s?(\d+)(?:\'|,|\’|foot)\s?(\d+)*(?:\"|\'\'|\s|inches|&quot;|\”)*'
    bodyPatternFinder = re.compile(bodyInfoPattern, re.IGNORECASE)
    bodyMatches = bodyPatternFinder.match(postTitle)
    

def getPostData(postHTML):
    
    postData = {}  
    
    
    #Get Post Text Info and merge with postData
    postData.update(getPostTextInfo(postHTML))

    #Get Title
    postTitle = getPostTitle(postHTML)    
    postData['title'] = postTitle   
    
    #new Title Parsing tools
    titleData = tpt.getTitleInfo(postTitle)
    if len(titleData) > 0:
        postData.update(titleData)
    else:
        return -1

    #Temporary Thing
    #postTitleData = getPostTitleData(postTitle)
    return postData    
    
    '''
    if len(postTitleData) == 0:
        postTitleData = getPostTitleManual(postTitle)
        
        #print 'Post Parsing Failed'
    if len(postTitleData) == 0:
        postData.update(postTitleData)
        #print postTitleData
        return postData
    return -1
    '''
    
def getNextPageHTML(fullHTML):
    nextHref = fullHTML.find('span', {'class':'nextprev'}).find('a',{'rel':'nofollow next'}).get('href')
    req = urllib2.Request(nextHref)
    req.add_header('User-Agent', 'Python:Insight ProgressPic Weight Prediction (by /u/gahathat)')
    page = urllib2.urlopen(req)   
    fullHTML = BeautifulSoup(page.read())
    
    return fullHTML