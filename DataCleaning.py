# 
# 
# We now need to convert all weights to lbs

# In[5]:



fullData.ix[fullData.weightUnit == 'kg',['startWeight','endWeight','weightChange']] = fullData.ix[fullData.weightUnit == 'kg',['startWeight','endWeight','weightChange']].applymap(lambda x: float(x)*2.2)
fullData.ix[fullData.weightUnit == 'kg',['startWeight','endWeight','weightChange']]


# The scraping success rate can show us how efficient the scraping process was per time range

# In[6]:

print scrapedSuccesses


# In[7]:

import pymysql as mdb
import sqlalchemy 

con = mdb.connect('localhost', 'root', '', 'RedditWeightDatabase') #host, user, password, #database
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS redditWeightTable")


sqlEngine = sqlalchemy.create_engine('mysql+pymysql://root@localhost/RedditWeightDatabase')

fullData.to_sql('redditWeightTable', sqlEngine)


# #Cleaning the Data
# 
# First, duplicates are removed

# In[10]:

print 'Fulldata shape (Before removing duplicates): ' + str(fullData.shape)
cleanedData = fullData.drop_duplicates()
print 'Fulldata shape (After removing duplicates): ' + str(cleanedData.shape)


# Next, the non-duplicated data is perused for outliers

# In[11]:

cleanedData.describe()


# There is a person with an end weight of 125,169. This must be an error. We find this entry to see what the problem was and then remove it:

# In[12]:

print cleanedData.ix[cleanedData.endWeight > 1000,:]

#Get the index of all samples with weight > 1,000
dropIndexes = cleanedData.endWeight > 1000
dropIndexes = dropIndexes[dropIndexes == True].index.map(lambda x: int(x))

#Drop all entries with this excessive weight
cleanedData = cleanedData.drop(dropIndexes, axis=0)
print 'New CleanedData shape: ' + str(cleanedData.shape)


# 
# Let's look at the data again, now that the outlier has been removed

# In[13]:

cleanedData.describe()


# Now, let's look at the entry where a user had a time elapsed of 2013.

# In[35]:

cleanedData.ix[cleanedData.TimeElapsed > 400,'title']


# It looks like this person put a year as their timeframe, let's just remove this:

# In[36]:

#Get the index of all samples with TimeElapsed > 400
dropTimeElapsedIndexes = cleanedData.TimeElapsed > 400
dropTimeElapsedIndexes = dropTimeElapsedIndexes[dropTimeElapsedIndexes == True].index.map(lambda x: int(x))

#Drop all entries with this excessive weight
cleanedData = cleanedData.drop(dropTimeElapsedIndexes, axis=0)
print 'New CleanedData shape: ' + str(cleanedData.shape)


# Investigating the data again

# In[37]:

cleanedData.describe()


# If someone is too old (> 100 years), this is likely a false entry:

# In[38]:

#Get the index of all samples with age > 100
dropIndexes = cleanedData.Age > 100
dropIndexes = dropIndexes[dropIndexes == True].index.map(lambda x: int(x))

#Drop all entries with this excessive weight
cleanedData = cleanedData.drop(dropIndexes, axis=0)
print 'New CleanedData shape after removing age > 100: ' + str(cleanedData.shape)


# ##Plotting the data

# In[39]:

import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 15,7

#plt.xlabel = 'Age'

#fullData.Age.hist(bins=np.arange(fullData.Age.min()-5,fullData.Age.max()+5,1))


plt.hist(cleanedData.Age,bins=np.arange(fullData.Age.min()-5,fullData.Age.max()+5,1), facecolor='g', alpha=0.8)
plt.suptitle('Age Distribution of Posters on r/ProgressPics', fontsize=20)
plt.xlabel('Age', fontsize=16)
plt.ylabel('Count', fontsize=16)


#                                          Age
# 
# Plotting a histogram for all of the data gathered:

# In[40]:

rcParams['figure.figsize'] = 15,15

#Generates a histogram for each column
cleanedData.hist()


# In[ ]:



