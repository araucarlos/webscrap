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


imf=pd.read_csv('autocasion220519.csv')

df_scat=imf[(imf['Modelo']=="Qashqai") & (imf['Combustible']=="Gasolina")][['Modelo','Precio','km','Meses']]


#exploratory analysis
plt.pyplot.scatter(df_scat['Meses'],df_scat['Precio'])
plt.pyplot.scatter(df_scat['km'],df_scat['Precio'])

#exploratory analysis, Precio vs km for Meses=24-36m
df_scat0_12=df_scat.loc[(df_scat['Meses'] >= 24) & (df_scat['Meses'] < 36)]
plt.pyplot.scatter(df_scat0_12['km'],df_scat0_12['Precio'])

#exploratory analysis, Precio vs Meses for km=40000-60000km
df_scat40k_60k=df_scat.loc[(df_scat['km'] >= 40000) & (df_scat['km'] < 60000)]
plt.pyplot.scatter(df_scat40k_60k['Meses'],df_scat40k_60k['Precio'])

#exploratory analysis, covariance between km vs Meses? Pearson correlation coeficient calculation
cor, p_value = pearsonr(df_scat['Meses'],df_scat['km'])
#strong correlation

#Linear Model
#holdout validation - Multiple linear model 'Precio' vs 'Meses' & 'km'

#1.train/test split. 30% goes to dataset
x_train,x_test,y_train,y_test=train_test_split(df_scat[['km','Meses']],df_scat['Precio'],test_size=0.3,random_state=0)

#2.linear regression
lm = linear_model.LinearRegression()
model1=lm.fit(x_train,y_train)
predictions_l_1=lm.predict(x_test)

#3.Plot the model
#3.1.Plot the model
plot = sns.scatterplot(y_test, predictions_l_1)
plot.set(xlabel='Given', ylabel='Prediction')
#3.2.Generate and graph y = x line
x_plot = np.linspace(10000,25000,10)
y_plot = x_plot
plt.pyplot.plot(x_plot, y_plot, color='r')

#4.Model score
Rsq_l_1= metrics.r2_score(y_test, predictions_l_1)

#k-fold cross validation - 3 fold model, Multiple linear

#2.linear regression
predictions_l_2=cross_val_predict(lm,df_scat[['km','Meses']],df_scat['Precio'],cv=3)

#3.Plot the model
#3.1.Plot the model
plot = sns.scatterplot(df_scat['Precio'], predictions_l_2)
plot.set(xlabel='Given', ylabel='Prediction')
#3.2.Generate and graph y = x line
x_plot = np.linspace(10000,25000,10)
y_plot = x_plot
plt.pyplot.plot(x_plot, y_plot, color='r')

#4.Model score
Rsq_l_2=cross_val_score(lm,df_scat[['km','Meses']],df_scat['Precio'],cv=3)

#Polynomical Model
#holdout validation - Multiple polynomial model 'Precio' vs 'Meses' & 'km'
#calculating different r2 values for different polynomial order
Rsq_pn_2=[]
order=[1,2,3]
for n in order:
    pr=PolynomialFeatures(degree=n)
    x_train_pr=pr.fit_transform(x_train)
    x_test_pr=pr.fit_transform(x_test)
    lm.fit(x_train_pr,y_train)
    predictions_pn_2=lm.predict(x_test_pr)
    Rsq_pn_2.append(metrics.r2_score(y_test,predictions_pn_2))
     
#with n=2,3 model improves
    
#Polynomial Model with n=3, holdout validation
#1.Convert the original features into their higher order terms
pr=PolynomialFeatures(degree=3)
x_train_pr=pr.fit_transform(x_train)
x_test_pr=pr.fit_transform(x_test)

#2.Train model using linear Regression over converted features
lm.fit(x_train_pr,y_train)
predictions_p3_2=lm.predict(x_test_pr)

#3.Plot the model
#Plot the model with n=3
plot = sns.scatterplot(y_test, predictions_p3_2)
plot.set(xlabel='Given', ylabel='Prediction')
#Generate and graph y = x line
x_plot = np.linspace(10000,25000,10)
y_plot = x_plot
plt.pyplot.plot(x_plot,y_plot,'r-')

#4.Model score
Rsq_p3_2=metrics.r2_score(y_test,predictions_p3_2)


#exponential model - 1 variable, train/test split

#1.train/test split. 30% goes to test dataset
x_train,x_test,y_train,y_test=train_test_split(df_scat['Meses'],df_scat['Precio'],test_size=0.3,random_state=0)

#2.Define the function
def func(x, a, b, c):
    return a * np.exp(-b * x) + c

#3.Train model using exponential function
popt, pcov = curve_fit(func,x_train,y_train,p0=[1000, 1, 10000])
predictions_e_1=func(x_test, *popt)

#4.Plot the model
plot = sns.scatterplot(y_test, predictions_e_1)
plot.set(xlabel='Given', ylabel='Prediction')

#5.Model score
Rsq_e_1=metrics.r2_score(y_test,predictions_e_1)


#exponential model - 2 variable
#1.train/test split. 30% goes to test dataset
x_train,x_test,y_train,y_test=train_test_split(df_scat[['km','Meses']],df_scat['Precio'],test_size=0.3,random_state=0)

#2.Define the function
def func2(X, a, b, c, d, e):
    x,y=X
    return a * np.exp(-b * x) + c * np.exp(-d * y) + e

#3.Train model using exponential function
popt, pcov = curve_fit(func2,(x_train['Meses'],x_train['km']),y_train,p0=[16450.35, 0.005838, 5773.00, 0.00001617, 550.69])
predictions_e_2=func2((x_test['Meses'],x_test['km']), *popt)

#4.Plot the model
plot = sns.scatterplot(y_test, predictions_e_2)
plot.set(xlabel='Given', ylabel='Prediction')

#5.Model score
Rsq_e_2=metrics.r2_score(y_test,predictions_e_2)

