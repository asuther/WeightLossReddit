import DataCleaningTools as dct
import pandas as pd
 
 
# We now need to convert all weights to lbs
columnNames = ['Gender','Age','Height','startWeight','endWeight','weightChange','weightUnit',
              'TimeElapsed','TimeUnit','userText','username','title','commentCount',
              'votes','postDateTime','postURL']
rawData = pd.DataFrame(data, columns=columnNames)

#Convert all weights to pounds
rawData = dct.convertWeightToPounds(rawData)

# First, duplicate rows are removed
print 'Fulldata shape (Before removing duplicates): ' + str(rawData.shape)
cleanedData = rawData.drop_duplicates()
print 'Fulldata shape (After removing duplicates): ' + str(cleanedData.shape)


# There is a person with an end weight of 125,169. This must be an error. We find this entry to see what the problem was and then remove it:
cleanedData = dct.removeOutliersByColumn(cleanedData, 'endWeight', minValue=50, maxValue=1000)

# It looks like this person put a year as their timeframe, let's just remove this:

#Get the index of all samples with TimeElapsed > 400
cleanedData = dct.removeOutliersByColumn(cleanedData, 'TimeElapsed', maxValue=400)

# If someone is too old (> 100 years), this is likely a false entry:
cleanedData = dct.removeOutliersByColumn(cleanedData, 'Age', maxValue=100)

cleanedData = dct.removeDataWithoutTimeUnit(cleanedData)

cleanedData = dct.convertTimeElapsedToEpoch(cleanedData)

cleanedData = dct.convertMaleFemaleToMF(cleanedData)

cleanedData = dct.removeMissingWeightRows(cleanedData)

fullData = cleanedData.copy()