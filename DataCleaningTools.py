# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 13:23:58 2015

@author: alexsutherland
"""

import datetime
import unicodedata

def convertWeightToPounds(data):
    
    kgIndexes = data.weightUnit == 'kg'
    data.ix[kgIndexes,['startWeight','endWeight','weightChange']] = data.ix[kgIndexes,['startWeight','endWeight','weightChange']].applymap(lambda x: float(x)*2.2)
    data.ix[kgIndexes,'weightUnit'] = 'lb'
    
    return data

def removeOutliersByColumn(data, columnName, minValue='', maxValue=''):
    initialRows = data.shape[0]
    print str(minValue) + ' > ' + columnName + ' > ' + str(maxValue) + '...',
    if type(minValue) == int:
        dropIndexes = data[columnName] < minValue
        dropIndexes = dropIndexes[dropIndexes == True].index.map(lambda x: int(x))
    
        #Drop all entries with this excessive weight
        data = data.drop(dropIndexes, axis=0)
    if type(maxValue) == int:
        dropIndexes = data[columnName] > maxValue
        dropIndexes = dropIndexes[dropIndexes == True].index.map(lambda x: int(x))
    
        #Drop all entries with this excessive weight
        data = data.drop(dropIndexes, axis=0)
    print 'Removed ' + str(initialRows - data.shape[0]) + ' outliers from ' + columnName + '. Shape: ' + str(data.shape)
    
    return data

def convertTimeElapsedToEpoch(data):
    print 'Adding column for time elapsed in Epoch'
    conversionFactors = {'mo': 2600000, 'da': 86400,'ye': 31504000, 'yr': 31504000, 'we': 604800}
    
    data['timeElapsedEpoch'] = data.apply(lambda x: x['timeElapsed'] * conversionFactors[(x['timeUnit'].lower()[0:2])] , axis=1)
    
    return data

def convertDateTimeToEpochTime(fullDatetime):
    #print 'Adding column for post time in Epoch'
    
    ymd = fullDatetime.split('T')[0]
    splitTimeData = map(lambda x: int(x), ymd.split('-'))
    return int(datetime.datetime(splitTimeData[0], splitTimeData[1], splitTimeData[2],0,0).strftime('%s'))

def removeDataWithoutTimeUnit(data):
    initialRows = data.shape[0]    
    
    dropIndexes = data['timeUnit'].map(lambda x: x is None)
    dropIndexes = dropIndexes[dropIndexes == True].index.map(lambda x: int(x))

    data = data.drop(dropIndexes, axis=0)
    
    print 'Removed ' + str(initialRows - data.shape[0]) + ' samples without TimeUnits. Shape: ' + str(data.shape)
    return data

def convertMaleFemaleToMF(data):
    print 'Converting coding to Male-->M and Female-->F'
    data['gender'] = data['gender'].map(lambda x: x[0].upper())
    
    return data
    
def removeMissingWeightRows(data):
    initialRows = data.shape[0]    

    dropIndexes = data['weightUnit'] == ''
    dropIndexes = dropIndexes[dropIndexes == True].index.map(lambda x: int(x))

    data = data.drop(dropIndexes, axis=0)
    
    print 'Removed ' + str(initialRows - data.shape[0]) + ' samples without WeightUnits. Shape: ' + str(data.shape)

    return data

def fillInMissingWeightUnit(data):

    #Full in ones that mention lbs
    dataWithMissingWeightUnit = data.ix[data['weightUnit'] == '',]
    
    initialRowsWithoutWeightUnit = dataWithMissingWeightUnit.shape[0]
    
    foundLbsArray = dataWithMissingWeightUnit.ix[dataWithMissingWeightUnit['title'].map(lambda x: True if x.lower().find('lb') > 0 else False),'title']
    
    data.ix[foundLbsArray.index,'weightUnit'] = 'lb'
    
    #Fill in data where the weight could not be kgs
    dataWithMissingWeightUnit = data.ix[data['weightUnit'] == '',]
    
    largeWeightArray = dataWithMissingWeightUnit.ix[dataWithMissingWeightUnit['startWeight'].map(lambda x: True if x > 140 else False),'title']
    
    data.ix[largeWeightArray.index,'weightUnit'] = 'lb'
    
    finalRowsWithoutWeightUnit = data.ix[data['weightUnit'] == '',].shape[0]

    print 'Filled in ' + str(initialRowsWithoutWeightUnit - finalRowsWithoutWeightUnit) + ' samples with new WeightUnits. Shape: ' + str(data.shape)
    
    return data

def cleanTitles(data):
    
    data['title'] = data['title'].map(lambda x: unicodedata.normalize('NFKD', unicode(x, 'utf-8')).encode('ascii','ignore'))
    data['userText'] = data['userText'].map(lambda x: unicodedata.normalize('NFKD', unicode(x, 'utf-8')).encode('ascii','ignore'))
    
    return data
