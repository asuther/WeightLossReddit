library(gplots)

setwd('/Users/alexsutherland/Dropbox/Insight/WeightLossReddit')
fullData = read.csv('Data/combinedSentiment.csv')
truncatedData = subset(fullData, select=-c(gender,endWeight, currentBMI, author,title,userText,X,name,url,permalink,created_utc,weightUnit,over_18,timeElapsed,timeUnit,timeElapsedEpoch,username))


heatmap.2(as.matrix(cor(truncatedData)), col=redgreen(75), 
          density.info="none", trace="none", dendrogram=c("row"), 
          symm=F,symkey=T,symbreaks=T, scale="none") 