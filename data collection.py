# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 16:21:42 2021

@author: Youssef
"""

import testt as gs
import pandas as pd
path = "C:/Users/Youssef/Documents/ds_salary_proj/chromedriver"

df = gs.get_jobs('data scientist','US',15,False,path,5)