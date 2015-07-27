# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 15:27:38 2015

@author: alexsutherland
"""
import sys
sys.path.append('/Users/alexsutherland/Dropbox/Insight/WeightLossReddit')
import time
import re
import numpy as np
from BeautifulSoup import BeautifulSoup
import urllib2
import redditDataIO
from selenium import webdriver


def filterURLs(data):
    #data.ix[data['postURL'] ]

    singleImgurPattern = re.compile('imgur\.com\/[A-Za-z0-9]{5,8}$', re.IGNORECASE)
    singleImgurIndexes = data['postURL'].map(lambda x: len(re.findall(singleImgurPattern, x)) > 0)
    data.ix[singleImgurIndexes, 'postURL'] = data.ix[singleImgurIndexes, 'postURL'].map(lambda x: x + '.png')
    
    
    pattern = re.compile('http://.*\/.*\.(jpg|png|jpeg)', re.IGNORECASE)
    goodURLIndexes = data['postURL'].map(lambda x: len(re.findall(pattern, x)) > 0)
    
    return data.ix[goodURLIndexes,:]

def getImgurLink(imgurURL):
    req = urllib2.Request(imgurURL)
    page = urllib2.urlopen(req)

    fullHTML = BeautifulSoup(page.read())
    
    imageContainer = fullHTML.findAll('img')
        

def getBeforeAndAfterAge(imageURL):
    
    #imageURL = 'http://i.imgur.com/upUBBc2.jpg' #Guy
    #imageURL = 'http://i.imgur.com/d7sYj6J.jpg' #Girl
    
    #driver = webdriver.Chrome()
    print imageURL
    driver = webdriver.Chrome('/Users/alexsutherland/Documents/Programming/Python/chromedriver')
    driver.get("http://how-old.net/?q=corey+duffel#")
    
    image = driver.find_element_by_class_name("selectedImage")
    scriptText = 'arguments[0].setAttribute("data-url","' + imageURL + '");'
    driver.execute_script(scriptText, image) 
    
    time.sleep(1)
    submitButton = driver.find_element_by_css_selector('[onclick="analyzeUrl() "]')
    submitButton.click()
    time.sleep(8)
    
    ageTooltips = driver.find_elements_by_css_selector('[role="tooltip"]')
    positionString = r'left: (\d+)'
    positionPatternCompile = re.compile(positionString, re.IGNORECASE)
    
    positions = []
    for ageTooltip in ageTooltips:
        tooltipStyle = ageTooltip.get_attribute('style')
        positionMatch = positionPatternCompile.findall(tooltipStyle)
        positions.append(int(positionMatch[0]))
    
    ageElements = driver.find_elements_by_class_name('tooltip-inner')
    
    agePatternString = r'(\d+)'
    agePatternCompile = re.compile(agePatternString, re.IGNORECASE)
    
    ages = []
    for ageElement in ageElements:
        ageElementText = ageElement.get_attribute('innerHTML')
        ageTextMatches = agePatternCompile.findall(ageElementText)
        ages.append(int(ageTextMatches[0]))
    
    
    driver.close()
    
    ageData = {}
    
    if len(positions) == 2:
        #Set the order
        if positions[1] > positions[0]:
            ageData['beforeAge'] = ages[0]
            ageData['afterAge'] = ages[1]
        else:
            ageData['beforeAge'] = ages[1]
            ageData['afterAge'] = ages[0]
    else:
        return {}
    #print ageData
    
    return ageData
    #ageData = pd.DataFrame(zip(positions,ages), columns=['position','ages'])
    #print ageData
    #time.sleep(2)
rawData = redditDataIO.loadData('combinedSentiment')
rawData = rawData.ix[rawData['over_18'] == 0,['username','url']]

rawData.columns = ['username','postURL']
goodURLData = filterURLs(rawData)

goodURLData = goodURLData.ix[:,['username','postURL']]

fullAgeData = []
for usernameURLInfo in goodURLData.iterrows():
    #imgLink = getImgurLink(usernameURLInfo[1]['postURL'])
    ageData = getBeforeAndAfterAge(usernameURLInfo[1]['postURL'])
    if len(ageData) > 0:
        ageData['username'] = usernameURLInfo[1]['username']
        ageData['URL'] = usernameURLInfo[1]['postURL']
        fullAgeData.append(ageData)
    print ageData

#getImgurLink('http://imgur.com/b3Ug3')