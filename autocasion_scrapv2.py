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
import matplotlib as plt


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
        soup3=soup2.find('ul', {'class': "datos-basicos-ficha"})
        for ad3 in soup3.find_all('span'):
            Result2=Result2+[ad3.text.strip().encode('utf-8')] 
        Result=Result+[Result2]
        
driver.quit()
df=pd.DataFrame(Result)

#preprocesing


tf=df
tf=tf.drop(columns=[2,4,6,8,10,12,14,16,18])
tf.columns=["Vehiculo","Precio","Fecha matriculacion","Combustible","km","Carroceria","Cambio","Potencia","Garantia","Color","Distintivo ambiental"]
tf["Marca"]=""
tf["Modelo"]=""
tf["Version"]=""
tf["Traccion"]=""
column_names = ["Vehiculo", "Marca", "Modelo","Version","Traccion","Precio","Fecha matriculacion","Combustible","km","Carroceria","Cambio","Potencia","Garantia","Color","Distintivo ambiental"]
tf = tf.reindex(columns=column_names)


for i, row in tf.iterrows():
    row[1]="NISSAN"
    if "qashqai" in row[0].lower():
        row[2]="Qashqai"
    elif "x-trail" in row[0].lower():
        row[2]="X-Trail"
    elif "juke" in row[0].lower():
        row[2]="Juke"  
    elif "micra" in row[0].lower():
        row[2]="Micra"
    elif "leaf" in row[0].lower():
        row[2]="Leaf"
    elif "pulsar" in row[0].lower():
        row[2]="Pulsar" 
    elif "note" in row[0].lower():
        row[2]="Note"
    elif "navara" in row[0].lower():
        row[2]="Navara"
    elif "murano" in row[0].lower():
        row[2]="Murano"  
    else:
        row[2]=""
    if "visia" in row[0].lower():
        row[3]="Visia"
    elif "acenta" in row[0].lower():
        row[3]="Acenta"
    elif "n-connecta" in row[0].lower():
        row[3]="N-Connecta"
    elif "tekna" in row[0].lower():
        row[3]="Tekna"
    else:
        row[3]=""
    if "4x4" in row[0]:
        row[4]="4x4"
    else:
        row[4]="4x2"   
    if type(row[5])==float:
        pass
    else: 
        row[5]=row[5].strip("\xe2\x82\xac")
        row[5]=row[5].strip(" ")
        row[5]=float(row[5])*1000
    row[8]=row[8].strip("km")
    row[8]=row[8].strip(" ")
    row[8]=row[8].replace(".","")
    row[8]=float(row[8])
    try:
        row[11]=float(row[11])
    except:
        row[11]=""
    if len(row[6])==4:
        row[6]="01/"+row[6]
    else:
        pass
    if row[12]=="Sí":
        pass
    elif row[12]=="No":
        row[12]=float(0)
    else:
        row[12]=row[12].strip("meses")
        row[12]=row[12].strip(" ")
        row[12]=float(row[12])

tf['Fecha matriculacion']=pd.to_datetime(tf['Fecha matriculacion'], format='%m/%Y')
tf['Meses']=((pd.to_datetime("today")- tf['Fecha matriculacion'])/np.timedelta64(1, 'M')).astype('int')

tf.to_csv('autocasion.csv', encoding='utf-8')



