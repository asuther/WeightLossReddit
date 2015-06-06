# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 13:51:36 2015

@author: alexsutherland
"""


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



