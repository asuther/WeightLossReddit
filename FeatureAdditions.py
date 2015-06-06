import datetime

#Note: The data should be named "data"

#Add BMI Information to the dataset
fullData['currentBMI'] = (fullData['endWeight'] * 0.45) / ((fullData['Height']*0.025)**2)
fullData['previousBMI'] = (fullData['startWeight'] * 0.45) / ((fullData['Height']*0.025)**2)

#Calculate the approximate start date of their weight loss transformation
time.strptime(fullData.ix[1,'postDateTime'].split('T')[0], "%Y-%m-%d")

def getEpochTime(fullDatetime): 
    ymd = fullDatetime.split('T')[0]
    splitTimeData = map(lambda x: int(x), ymd.split('-'))
    return int(datetime.datetime(splitTimeData[0], splitTimeData[1], splitTimeData[2],0,0).strftime('%s'))
    
fullData['postEpochTime'] = fullData['postDateTime'].map(getEpochTime)

