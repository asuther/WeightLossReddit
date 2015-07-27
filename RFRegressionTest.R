setwd('/Users/alexsutherland/Dropbox/Insight/WeightLossReddit')
fullData = read.csv('Data/7.6.15 - Data.csv')

#Gathering Data
truncatedData = subset(fullData, select=-c(score, timeElapsedMonths, weightChangeRate, endWeight, currentBMI, author,title,userText,X,name,url,permalink,created_utc,weightUnit,over_18,timeElapsed,timeUnit,timeElapsedEpoch,username))
truncatedData = subset(truncatedData, select=-c(num_comments, previousBMI, fitnessCommentCount))
truncatedData$weightChange = truncatedData$weightChange * -1

totalSamples = dim(truncatedData)[1]

library(randomForest)
rf.fit = randomForest(weightChange ~ age + height + startWeight + gender, truncatedData, 
                      importance = TRUE,
                      mtry = 2)
varImpPlot(rf.fit)