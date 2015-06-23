import urllib2
import redditScrapingTools as rst
import pandas as pd
import redditDataIO as dataIO
import BeautifulSoup as bs
import time


#fullData = dataIO.loadData('fullCommentData')
fullData = pd.read_csv('Data/6.20.15-UserComment.csv')
subredditList = fullData['subreddit'].unique()

subredditSubscriberList = []

for index, subredditName in enumerate(subredditList[9457:]):
    print str(index) + ' out of ' + str(len(subredditList)) + ' subreddits scraped'
    currentSubredditData = []
    
    if type(subredditName) == str:
        try:
            float(subredditName)
        except ValueError: 
            requestURL = 'https://www.reddit.com/r/' + subredditName
            
            print requestURL
            
            req = urllib2.Request(requestURL)
            req.add_header('User-Agent', 'Python:Insight ProgressPic Weight Prediction (by /u/gahathat)')
            try:        
                page = urllib2.urlopen(req)
            except:
                pass
            
            pageHTML = bs.BeautifulSoup(page.read())
            
            #subNumber = 
            for item in pageHTML.findAll('span',{'class':'subscribers'}):
                for subItem in item.findAll('span',{'class':'number'}):
                    subNumber = int(subItem.contents[0].replace(',',''))
                    subredditSubscriberList.append([subredditName,subNumber])
            time.sleep(2)
            
fullSubredditSubscriberList = pd.DataFrame(subredditSubscriberList, columns=['subreddit','subscribers'])
