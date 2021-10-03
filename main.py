# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 17:55:20 2021

@author: oming
"""


import glassdoor_scraper as gs
import pandas as pd

path = "D:\\Downloads\\chromedriver_win32\\chromedriver"

df = gs.get_jobs("data engineer", 1000, path, 15)
 
df.to_csv("glassdoor_jobs.csv", index=False)






