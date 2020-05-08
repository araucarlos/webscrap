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
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict


imf=pd.read_csv('autocasion_060519.csv')

df_scat=imf[imf['Modelo']=="Qashqai"][['Modelo','Precio','km','Meses']]


#exploratory analysis
plt.pyplot.scatter(df_scat['Meses'],df_scat['Precio'])
plt.pyplot.scatter(df_scat['km'],df_scat['Precio'])

#data modeling
#model evaluation by visualization
sns.residplot(df_scat['Meses'],df_scat['Precio'])
sns.residplot(df_scat['km'],df_scat['Precio'])
#non of them linear

#holdout validation - Multiple linear model 'Precio' vs 'Meses' & 'km'

#1.train/test split. 30% goes to dataset
x_train,x_test,y_train,y_test=train_test_split(df_scat[['km','Meses']],df_scat['Precio'],test_size=0.3,random_state=0)

#2.linear regression
lm = linear_model.LinearRegression()
model1=lm.fit(x_train,y_train)
predictions1=lm.predict(x_test)
print predictions1

#3.Plot the model
#3.1.Plot the model
plot = sns.scatterplot(y_test, predictions1)
plot.set(xlabel='Given', ylabel='Prediction')
#3.2.Generate and graph y = x line
x_plot = np.linspace(10000,25000,10)
y_plot = x_plot
plt.pyplot.plot(x_plot, y_plot, color='r')

#4.Model score
mse1 = metrics.mean_squared_error(y_test, predictions1)


#k-fold cross validation - 3 fold model

#2.linear regression
predictions2=cross_val_predict(lm,df_scat[['km','Meses']],df_scat['Precio'],cv=3)

#3.Plot the model
#3.1.Plot the model
plot = sns.scatterplot(df_scat['Precio'], predictions2)
plot.set(xlabel='Given', ylabel='Prediction')
#3.2.Generate and graph y = x line
x_plot = np.linspace(10000,25000,10)
y_plot = x_plot
plt.pyplot.plot(x_plot, y_plot, color='r')

#4.Model score
scores=cross_val_score(lm,df_scat[['km','Meses']],df_scat['Precio'],cv=3)

