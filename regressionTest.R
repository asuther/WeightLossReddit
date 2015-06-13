library(GGally)

setwd('/Users/alexsutherland/Dropbox/Insight/WeightLossReddit')
fullData = read.csv('fullData.csv')
fullData = fullData[fullData['weightChange'] > 2,]

#maleLossData = fullData[fullData['weightChange'] > 2,]
#maleLossData = maleLossData[maleLossData['Gender'] == 'M',]

truncatedData = fullData[,-c(1,6,8,10,11)]
#truncatedData$Male = dummy.coef(maleLossData2$Gender)


#truncatedData = fullData[1:500,]
#truncatedData = data.frame(cbind(1:10, c(1,3,3,4,5,6,5,8,8,10)))

totalSamples = dim(truncatedData)[1]

trainIndexes = sample(1:totalSamples, totalSamples * 0.8)
trainData = truncatedData[trainIndexes,]
testData = truncatedData[-trainIndexes,]

lm.fit = lm(weightChange ~ Gender + Age + Height + startWeight , data = trainData)

lm.predict = predict(lm.fit, newdata = testData)

RMSE = sqrt(sum((lm.predict - testData[,'weightChange'])^2) / dim(testData)[1])

colorEncoding = ifelse(abs(rstudent(lm.fit)) > 3, 2, 1)

plot(testData[,'weightChange'], lm.predict, col=testData$Gender)
 
print(paste('RMSE: ', RMSE))
