library(GGally)
library(glmnet)

setwd('/Users/alexsutherland/Dropbox/Insight/WeightLossReddit')
fullData = read.csv('Data/combinedSentiment.csv')

#maleLossData = fullData[fullData['weightChange'] > 2,]
#maleLossData = maleLossData[maleLossData['Gender'] == 'M',]

truncatedData = subset(fullData, select=-c(score, timeElapsedMonths, weightChangeRate, endWeight, currentBMI, author,title,userText,X,name,url,permalink,created_utc,weightUnit,over_18,timeElapsed,timeUnit,timeElapsedEpoch,username))
#Removing Collinear vars
truncatedData = subset(truncatedData, select=-c(num_comments, previousBMI, fitnessCommentCount))

#truncatedData$Male = dummy.coef(maleLossData2$Gender)


#truncatedData = fullData[1:500,]
#truncatedData = data.frame(cbind(1:10, c(1,3,3,4,5,6,5,8,8,10)))

totalSamples = dim(truncatedData)[1]
lambdaList = c()
RMSEList = c()

for (i in 1:500) {
  trainIndexes = sample(1 : totalSamples, totalSamples * 0.8)
  trainData = truncatedData[trainIndexes,]
  testData = truncatedData[-trainIndexes,]
  
  lm.fit = lm(weightChange ~ startWeight+height, data = trainData)
  
  lm.predict = predict(lm.fit, newdata = testData)
  
  RMSE = sqrt(sum((lm.predict - testData[,'weightChange'])^2) / dim(testData)[1])
  
  colorEncoding = ifelse(abs(rstudent(lm.fit)) > 3, 2, 1)
  
  plot(testData[,'weightChange'], lm.predict, col=testData$gender)
   
  #print(paste('RMSE: ', RMSE))
  
  RMSEList = c(RMSE, RMSEList)

}

plot(testData[,'weightChange'], lm.predict, col=testData$gender)

#hist(RMSEList)
print(summary(lm.fit))
print(mean(RMSEList))

