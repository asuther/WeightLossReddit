import datetime

#Note: The data should be named "fullData"


def addFeatures(fullData):
    
    #Add BMI Information to the dataset
    fullData['currentBMI'] = (fullData['endWeight'] * 0.45) / ((fullData['height']*0.025)**2)
    fullData['previousBMI'] = (fullData['startWeight'] * 0.45) / ((fullData['height']*0.025)**2)
    
    return fullData