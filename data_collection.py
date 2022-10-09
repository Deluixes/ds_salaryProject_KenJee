# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 22:26:04 2022

@author: jdaul
"""

import glassdoor_scraper as gs
import pandas as pd

path = "C:/Users/jdaul/Documents/Machine Learning Deep Learning/Machine Learning projects/Salary_project_Ken_Jee/chromedriver"

df = gs.get_jobs('data_scientist', 10, False, path, 5)