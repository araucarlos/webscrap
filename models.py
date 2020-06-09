#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 18:37:10 2020

@author: carlosarau
"""

import pandas as pd
import numpy as np
import matplotlib as plt
from datetime import datetime
import csv
from sklearn import linear_model, metrics
from sklearn.preprocessing import PolynomialFeatures
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
from scipy.optimize import curve_fit
from scipy.stats import pearsonr

def func2(x, a, b):
    return a * np.exp(-b * x)

class Exponential():
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        x_train,x_test,y_train,y_test=train_test_split(self.x,self.y,test_size=0.3,random_state=0)
        self.popt,self.pcov = curve_fit(func2,x_train['months'],y_train,p0=[16450.35, 0.008])
        predictions=func2(x_test['months'], *self.popt)
        self.Rsq=metrics.r2_score(y_test,predictions)        
        
    def predictions(self,months):
        result=func2(pd.DataFrame([months]), *self.popt)
        return result
