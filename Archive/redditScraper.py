"""
User-Agent: Python:Insight ProgressPic Weight Prediction (by /u/gahathat)
"""

import requests
import pandas as pd

r = requests.get(r'http://www.reddit.com/user/spilcm/comments/.json')

data = r.json()

