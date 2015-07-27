# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 15:27:38 2015

@author: alexsutherland
"""
import time
import re
import numpy as np
import redditDataIO

from selenium import webdriver

def getBeforeAndAfterAge(imageURL):
    
    #imageURL = 'http://i.imgur.com/upUBBc2.jpg' #Guy
    #imageURL = 'http://i.imgur.com/d7sYj6J.jpg' #Girl
    
    #driver = webdriver.Chrome()
    driver = webdriver.Chrome('/Users/alexsutherland/Documents/Programming/Python/chromedriver')
    driver.get("http://how-old.net/?q=corey+duffel#")
    
    image = driver.find_element_by_class_name("selectedImage")
    scriptText = 'arguments[0].setAttribute("data-url","' + imageURL + '");'
    driver.execute_script(scriptText, image) 
    
    time.sleep(1)
    submitButton = driver.find_element_by_css_selector('[onclick="analyzeUrl() "]')
    submitButton.click()
    time.sleep(3)
    
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
    
    ageData = {}
    if len(positions) == 2:
        #Set the order
        if positions[1] > positions[0]:
            ageData['beforeAge'] = ages[0]
            ageData['afterAge'] = ages[1]
        else:
            ageData['beforeAge'] = ages[1]
            ageData['afterAge'] = ages[0]
    
    print ageData
    driver.close()
    
    return ageData
    #ageData = pd.DataFrame(zip(positions,ages), columns=['position','ages'])
    #print ageData
    #time.sleep(2)



for imageURL in imageURLList:
    getBeforeAndAfterAge(imageURL)