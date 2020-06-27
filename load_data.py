#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 13:09:17 2020

@author: carlosarau
"""

import os
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from offers import *
import csv

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://postgres:mejor2@localhost:5432/autocasion"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
db.init_app(app)

def main():
	f=open("autocasion220519.csv")
	reader=csv.reader(f)
	for id, vehicle, brand, model, grade, drive, price, registration_date, fuel, mileage, body_type, transmission, horse_power, warranty, eco_label, months in reader:
		if vehicle=="Vehiculo":
			pass
		else:
			offer=Offer(vehicle=vehicle, brand=brand, model=model, grade=grade, drive=drive, price=price, registration_date=registration_date, fuel=fuel, mileage=mileage, body_type=body_type, transmission=transmission, horse_power=horse_power, warranty=warranty, eco_label=eco_label, months=months)
			db.session.add(offer)
	db.session.commit()

if __name__=="__main__":
	with app.app_context():
		main()