# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 13:23:58 2015

@author: alexsutherland
"""

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
    conversionFactors = {'mon': 2600000, 'mo': 2600000, 'day': 86400,'yea': 31504000, 'wee': 604800}
    
    data['TimeElapsedEpoch'] = data.apply(lambda x: x['TimeElapsed'] * conversionFactors[(x['TimeUnit'].lower()[0:3])] , axis=1)
    
    return data
    
def removeDataWithoutTimeUnit(data):
    initialRows = data.shape[0]    
    
    dropIndexes = data['TimeUnit'].map(lambda x: x is None)
    dropIndexes = dropIndexes[dropIndexes == True].index.map(lambda x: int(x))

    data = data.drop(dropIndexes, axis=0)
    
    print 'Removed ' + str(initialRows - data.shape[0]) + ' samples without TimeUnits. Shape: ' + str(data.shape)
    return data

def convertMaleFemaleToMF(data):
    print 'Converting coding to Male-->M and Female-->F'
    data['Gender'] = data['Gender'].map(lambda x: x[0].upper())
    
    return data
    
def removeMissingWeightRows(data):
    initialRows = data.shape[0]    

    dropIndexes = data['weightUnit'] == ''
    dropIndexes = dropIndexes[dropIndexes == True].index.map(lambda x: int(x))

    data = data.drop(dropIndexes, axis=0)
    
    print 'Removed ' + str(initialRows - data.shape[0]) + ' samples without WeightUnits. Shape: ' + str(data.shape)

    return data