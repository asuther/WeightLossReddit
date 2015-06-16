# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 13:04:40 2015

@author: alexsutherland
"""

import urllib2
from BeautifulSoup import BeautifulSoup
import re
import titleParsingTools as tpt
import json
import unicodedata

baseURL = 'https://www.reddit.com/r/progresspics/search/.json?restrict_sr=on&sort=relevance&limit=100&t=all&syntax=cloudsearch&q=%28and+title:%27%27%29+timestamp:'

#TimeStamp Info
timeStampJune2015 = 1433317589  #This is June 1st, 2015
timeStampJune2013 = 1370072789  #June 1st, 2013
monthTime = 2592000             #This is the approximate timespan of a month in seconds
postTitlePatternString = '(M|F|male|female)\s?\/\s?(\d+)\s?\/\s?(\d+)(?:\'|,|\’|foot)\s?(\d+)*(?:\"|\'\'|\s|inches|&quot;|\”)*.*(?:\[|\()(\d+)[\s]?(kg|lb)?[^\d]+(\d+)[\s]?(kg|lb|lbs)?(?:[^\d]*\=[^\d]*(\d+)[\s]?(kg|lb|lbs)?.*)?(?:\]|\))\s?(?:\[|\(|\s)[^\d]*(\d+)[.]?(\d+)?\s?(months|weeks|mo|month|week|year|years|days)?\s?(?:\)|\]|\s)\s?(.*)'

def getJSONData(timestampStart):
    
    timestampRange = str(timestampStart) + '..' + str(timestampStart + monthTime)   #Creates a string of the time range
    fullURL = baseURL+timestampRange
    print baseURL + timestampRange
    #Generates reddit request and gets full HTML of the search page
    req = urllib2.Request(fullURL)
    req.add_header('User-Agent', 'Python:Insight ProgressPic Weight Prediction (by /u/gahathat)')
    page = urllib2.urlopen(req)
    pageJSON = json.loads(page.read())  
    print page.read()
    
    return pageJSON, fullURL
    
def getPostTextInfo(postJSON):
    
    postTextData = {}
    
    postTextData = postJSON[['author','created_utc','num_comments','over_18','permalink','score','url','name']]
    
    return postTextData

def getPostTitle(postJSON):
    titleUnparsed = postJSON['title']
    
    title = str(unicodedata.normalize('NFKD', titleUnparsed).encode('ascii','ignore'))
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
    

def getPostData(postJSON):
    
    postData = {}  
    
    #Get Post Text Info and merge with postData
    postData.update(getPostTextInfo(postJSON))

    #Get Title
    postTitle = getPostTitle(postJSON)    
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

def getNextPageJSON(nextCode, fullURL, scrapeCount):

    fullURLAfter = fullURL + '&count=' + str(scrapeCount) + '&after=' + nextCode
    #print fullURLAfter
    
    #Generates reddit request and gets full JSON of the search page
    req = urllib2.Request(fullURLAfter)
    req.add_header('User-Agent', 'Python:Insight ProgressPic Weight Prediction (by /u/gahathat)')
    page = urllib2.urlopen(req)
    pageJSON = json.loads(page.read())  
    
    return pageJSON