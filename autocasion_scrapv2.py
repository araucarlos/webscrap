#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 16:46:08 2020

@author: carlosarau
"""

from bs4 import BeautifulSoup
import chromedriver_binary
from selenium import webdriver
import csv
from datetime import datetime
import pandas as pd
import numpy as np
import re

Result=[]
driver = webdriver.Chrome()
pages = np.arange(1, 2, 1)

for page in pages:
    
    url="https://www.autocasion.com/coches-segunda-mano/nissan-ocasion?page="+str(page)
    driver.get(url)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    for ad in soup.find_all('article', {'class': re.compile('anuncio')}):
        Result2=[ad.find('h2', {'itemprop': "name"}).text.strip().encode('utf-8')]+[ad.find('span', {'class': "price"}).text.strip().encode('utf-8')]
        r=ad.find('a', {'href': re.compile('ref')})
        urlv2="https://www.autocasion.com"+str(r['href'])
        driver.get(urlv2)
        html_source = driver.page_source
        soup2 = BeautifulSoup(html_source, 'html.parser')
        #Result2=[soup2.find('div', {'class': "precio"}).text.strip().encode('utf-8')]
        soup3=soup2.find('ul', {'class': "datos-basicos-ficha"})
        for ad3 in soup3.find_all('span'):
            Result2=Result2+[ad3.text.strip().encode('utf-8')] 
        Result=Result+[Result2]
    
driver.quit()
df=pd.DataFrame(Result)

#reprocesing


tf=df
tf=tf.drop(columns=[2,4,6,8,10,12,14,16,18])
tf.columns=["Vehiculo","Precio","Fecha matriculacion","Combustible","km","Carroceria","Cambio","Potencia","Garantia","Color","Distintivo ambiental"]

for i, row in tf.iterrows():

    if type(row[1])==float:
        pass
    else: 
        row[1]=row[1].strip("\xe2\x82\xac")
        row[1]=row[1].strip(" ")
        row[1]=float(row[1])*1000
    row[4]=row[4].strip("km")
    row[4]=row[4].strip(" ")
    row[4]=row[4].replace(".","")
    row[4]=float(row[4])
    row[7]=float(row[7])
    if row[8]=="Sí":
        pass
    elif row[8]=="No":
        row[8]=float(0)
    else:
        row[8]=row[8].strip("meses")
        row[8]=row[8].strip(" ")
        row[8]=float(row[8])

tf.to_csv('autocasion.csv', encoding='utf-8')



