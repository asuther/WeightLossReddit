library(GGally)
library(glmnet)

setwd('/Users/alexsutherland/Dropbox/Insight/WeightLossReddit')
fullData = read.csv('Data/combinedSentiment.csv')

#maleLossData = fullData[fullData['weightChange'] > 2,]
#maleLossData = maleLossData[maleLossData['Gender'] == 'M',]

truncatedData = subset(fullData, select=-c(score, timeElapsedMonths, weightChangeRate, endWeight, currentBMI, author,title,userText,X,name,url,permalink,created_utc,weightUnit,over_18,timeElapsed,timeUnit,timeElapsedEpoch,username))
#Removing Collinear vars
truncatedData = subset(truncatedData, select=-c(num_comments, previousBMI, fitnessCommentCount))
truncatedData$weightChange = truncatedData$weightChange * -1
#truncatedData$logStartWeight = log(truncatedData$startWeight)

#truncatedData$Male = dummy.coef(maleLossData2$Gender)


#truncatedData = fullData[1:500,]
#truncatedData = data.frame(cbind(1:10, c(1,3,3,4,5,6,5,8,8,10)))

totalSamples = dim(truncatedData)[1]
lambdaList = c()
RMSEList = c()

for ( i in 1:50 ) {
  trainIndexes = sample(1 : totalSamples, totalSamples * 0.8)
  trainData = truncatedData[trainIndexes,]
  testData = truncatedData[-trainIndexes,]
  
  lm.fit = lm(weightChange ~ startWeight:totalCommentCount + poly(startWeight,2) + height, data = trainData)
  
  lm.predict = predict(lm.fit, newdata = testData)
  
  RMSE = sqrt(sum((lm.predict - testData[,'weightChange'])^2) / dim(testData)[1])
  
  colorEncoding = ifelse(abs(rstudent(lm.fit)) > 3, 2, 1)
  
  #plot(testData[,'weightChange'], lm.predict, xlab='Weight Lost (lbs)')
  
  #print(paste('RMSE: ', RMSE))
  
  RMSEList = c(RMSE, RMSEList)
  
}


plot(testData[,'weightChange'], lm.predict, xlab='Actual Weight Lost (lbs)', ylab='Predicted Weight Lost (lbs)',
     main='Actual vs. Predicted Weight Lost using Linear Regression')
abline(a=0,b=1)

#hist(RMSEList)
print(summary(lm.fit))
print(mean(RMSEList))

