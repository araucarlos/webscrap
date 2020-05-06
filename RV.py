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


imf=pd.read_csv('autocasion.csv')

df_scat=imf[imf['Modelo']=="Qashqai"][['Modelo','Precio','km','Meses']]

plt.pyplot.scatter(df_scat['Meses'],df_scat['Precio'])
