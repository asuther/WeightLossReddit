# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 15:45:17 2015

@author: alexsutherland
"""

import requests
import pandas as pd
import xml.etree.ElementTree as ET

requestURL = 'http://svcs.ebay.com/services/search/FindingService/v1'

params = {'OPERATION-NAME' : 'findCompletedItems',
'SERVICE-VERSION':'1.0.0',
'SECURITY-APPNAME':'InsightD-14ce-4a9e-9402-bd7059db7d57',
'GLOBAL-ID':'EBAY-US',
'keywords':'ford',
'paginationInput.entriesPerPage': 3,
'categoryId':6001
}

eBayResponse = requests.get(requestURL, params=params)

root = ET.fromstring(eBayResponse.text)

