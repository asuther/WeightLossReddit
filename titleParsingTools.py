# -*- coding: utf-8 -*-

import re

#titleList = fullData['title']
#totalTitles = titleList.shape[0]

'''
********************
Weight Info Gathering/Parsing
*********************
'''

def gatherWeightInfoRegex(weightMatches):
    weightInfo = {}   
    weightUnit = ['','','']
    
    weightInfo['startWeight'] = int(weightMatches[0])
    weightUnit[0] = weightMatches[1]
    weightInfo['endWeight'] = int(weightMatches[2])
    weightUnit[1] = weightMatches[3]
    #if len(weightMatches[4]) > 0:
    #    weightInfo['weightChange'] = int(weightMatches[4])
    #else:
    weightInfo['weightChange'] = weightInfo['endWeight'] - weightInfo['startWeight']
        
    weightUnit[2] = weightMatches[5]
    
    weightInfo['weightUnit'] = getWeightUnit(weightUnit)
    
    return weightInfo

def getWeightUnit(weightUnitArray):
    weightUnit = ''    
    
    if len(weightUnitArray[0]) > 0:
        weightUnit = weightUnitArray[0][0:2].lower()
    elif len(weightUnitArray[1]) > 0:
        weightUnit = weightUnitArray[1][0:2].lower()
    elif len(weightUnitArray[2]) > 0:
        weightUnit = weightUnitArray[2][0:2].lower()
    
    return weightUnit

def gatherWeightInfoManual(title):
    
    SWCWPatternString = '[s|b]W\:?[^\d]*(\d+)(?:\.\d+)?\s?(kg|lb)?[^\d]*CW\:?\s?(\d+)(?:(?:\.\d+)?\s?(kg|lb)?[^\d]*GW:\s?(\d+)(?:\.\d+)?)?'
    weightPatternSW = re.compile(SWCWPatternString, re.IGNORECASE)
    
    weightInfo = {}
    weightUnit = ['','','']    
    #SW Method: (ex: SW: 250 CW: 160)
    weightSWMatchesDict = matchWithIndex(weightPatternSW, title)
    if len(weightSWMatchesDict['matches']) > 0:
        weightSWMatches = weightSWMatchesDict['matches']
        weightInfo['startWeight'] = int(weightSWMatches[0])
        weightUnit[0] = weightSWMatches[1]
        weightInfo['endWeight'] = int(weightSWMatches[2])
        weightUnit[1] = weightSWMatches[3]
        weightInfo['weightChange'] = weightInfo['endWeight'] - weightInfo['startWeight']
        
        weightInfo['weightUnit'] = getWeightUnit(weightUnit)
    #If the SW method did not work
    else:
        #Try the dash pattern (ex: 250 - 140)
        dashPattern = '(\d+)(?:\.\d+)?\s?(lb|lbs|kg|kgs|pounds)?\s?(?:\-|(?:\-)*\&gt\;|to)\s?(\d+)(?:\.\d+)?\s?(lb|lbs|kg|kgs|pounds)?'
        weightDashDict = matchWithIndex(re.compile(dashPattern, re.IGNORECASE), title)
        
        weightUnit = ['','','']
        weightInfo = {}
        if len(weightDashDict['matches']) > 0:
            weightDashMatches = weightDashDict['matches']

            weightInfo['startWeight'] = int(weightDashMatches[0])
            weightUnit[0] = weightDashMatches[1]
            weightInfo['endWeight'] = int(weightDashMatches[2])
            weightUnit[1] = weightDashMatches[3]
            weightInfo['weightChange'] = weightInfo['endWeight'] - weightInfo['startWeight']
            
            weightInfo['weightUnit'] = getWeightUnit(weightUnit)
        #print weightSWMatchesDict['matches'] 
    
    return weightInfo

def getWeightInfo(title):
    
    #Try the standard regex method
    weightPatternString = '(?:\[|\()[^\d]?(\d+)(?:\.\d+)?[\s]?(kg|lb|pounds)?[^\d]+(\d+)(?:\.\d+)?[\s]?(kg|lb|lbs|pounds)?(?:[^\d]*\=[^\d]*(\d+)(?:\.\d+)?[\s]?(kg|lb|lbs|pounds)?.*)?(?:\]|\))'    
    weightPattern = re.compile(weightPatternString, re.IGNORECASE)
    
    weightMatchDict = matchWithIndex(weightPattern, title)
    #print weightMatchDict    
    
    if len(weightMatchDict['matches']) > 0:
        weightInfo = gatherWeightInfoRegex(weightMatchDict['matches'])
    #If the regex did not work
    else:
        
        weightInfo = gatherWeightInfoManual(title)    
        
        
        
    return weightInfo
    
    
    
    weightInfoOpenBracketIndex = title.find('[',7,50)
    #If the open bracket was found    
    if not weightInfoOpenBracketIndex == -1:
        weightInfoClosedBracketIndex = title.find(']',weightInfoOpenBracketIndex, weightInfoOpenBracketIndex + 35 )
        
    else:
        pass

def matchWithIndex(pattern, s):
    startIndex = -1
    endIndex = -1
    
    matches = pattern.findall(s)
    #print matches
    
    if not matches == []:
        matches = matches[0]
        startIndex = s.find(matches[0])
        endIndex = s.find(matches[-1]) + len(matches[-1])
        
    return {'matches': matches, 'startIndex':startIndex, 'endIndex':endIndex}

'''
********************
Body Info Gathering/Parsing
*********************
'''
def getBodyInfo(title):
    
    bodyInfo = {}    
    
    #Compile the pattern
    bodyInfoPatternString = r'(M|F|male|female)\s?\/\s?(\d+)\s?\/\s?(\d+)(?:\'|,|\’|foot)\s?(\d+)*(?:\"|\'\'|\s|inches|&quot;|\”)*'
    bodyInfoPattern = re.compile(bodyInfoPatternString, re.IGNORECASE)

    bodyMatch = matchWithIndex(bodyInfoPattern, title)
        
    if len(bodyMatch['matches']) > 0:
        bodyMatches = bodyMatch['matches']
        bodyInfo['gender'] = bodyMatches[0][0].upper()
        bodyInfo['age'] = int(bodyMatches[1])
        
        if not bodyMatches[3] == '':
            bodyInfo['height'] = (int(bodyMatches[2])*12) + int(bodyMatches[3])
        #Else, there's only height in feet
        else:
            bodyInfo['height'] = int(bodyMatches[2])*12
    
    return bodyInfo
    
def getTimeElapsed(title):
    timeElapsedInfo = {}    
    
    numberDict = {
            'a': 1, 
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
            'five': 5,
            'six': 6,
            'seven': 7,
            'eight': 8,
            'nine': 9
            }    
    
    #Compile the pattern
    timeElapsedPatternString = '[\(|\[]?[^\d]?(\d+|one|a|two|three|four|five|six|seven|eight|nine)[\.|\,]?(\d+)?\s?(yr|yrs|years|year|weeks|week|month)[\)|\]]?(.*)'
    timeElapsedPattern = re.compile(timeElapsedPatternString, re.IGNORECASE)

    timeElapsedMatches = matchWithIndex(timeElapsedPattern, title)

        
    if len(timeElapsedMatches['matches']) > 0:
        
        timeElapsedMatches = timeElapsedMatches['matches']

        try:
            timeElapsedInt = float(timeElapsedMatches[0] + '.' + timeElapsedMatches[1] + '0')
        except ValueError:
            timeElapsedInt = numberDict[timeElapsedMatches[0].lower()]
        
        timeElapsedInfo['timeElapsed'] = timeElapsedInt
        timeElapsedInfo['timeUnit'] = timeElapsedMatches[2]
        timeElapsedInfo['userText'] = timeElapsedMatches[3]
        
    return timeElapsedInfo

def getTitleInfo(title):
    fullTitleData = {}    
    
    elapsedTimeData = getTimeElapsed(title)
    if len(elapsedTimeData) > 0:
        fullTitleData.update(elapsedTimeData)
        weightData = getWeightInfo(title)
        
        if len(weightData) > 0:
            fullTitleData.update(weightData)
            bodyData = getBodyInfo(title)
            
            if len(bodyData) > 0:
                fullTitleData.update(bodyData)
            else:
                fullTitleData = {}
                return fullTitleData
        else: 
            fullTitleData = {}
            return fullTitleData
                
    return fullTitleData
                
def titleTest():
    successfulTitles = 0
    for title in titleList:
    
        elapsedTimeData = getTimeElapsed(title)
        if len(elapsedTimeData) > 0:
            weightData = getWeightInfo(title)
            
            if len(weightData) > 0:
                bodyData = getBodyInfo(title)
                
                if len(bodyData) > 0:
                    successfulTitles += 1
                else:
                    print title
                
     
    print successfulTitles/float(totalTitles)   
