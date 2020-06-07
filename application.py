#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 13:09:17 2020

@author: carlosarau
"""

import os
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SelectField
from offers import *
from models import *
from decimal import Decimal

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://postgres:mejor2@localhost:5432/autocasion"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
db.init_app(app)

@app.route("/", methods=["GET","POST"])
def index():
	brand = db.session.query(Offer.brand).distinct()
	model = db.session.query(Offer.model).filter_by(brand='NISSAN').distinct()
	fuel = db.session.query(Offer.fuel).filter(and_(Offer.brand=='NISSAN', Offer.model=="Qashqai")).distinct()
	
	return render_template('index.html', brand=brand, model=model, fuel=fuel)

@app.route('/<model>')
def fuel(model):
	fuel=db.session.query(Offer.fuel).filter_by(model=model).distinct()

	fuelArray=[]

	for fuel in fuel:
		fuelObj={}
		fuelObj['name'] = fuel.fuel
		fuelArray.append(fuelObj)

	return jsonify({'fuel':fuelArray})

@app.route('/<model>/<fuel>/<months>/<mileage>')
def prediction(model,fuel,months,mileage):
	x=pd.DataFrame(db.session.query(Offer.months, Offer.mileage, Offer.price).filter(and_(Offer.model==model, Offer.fuel==fuel)).all())
	x.columns=["months","mileage","price"]
	x = x.apply(pd.to_numeric, errors='coerce')

	model=Exponential(x[['months']],x['price'])
	prediction = model.predictions(float(months))

	return jsonify({'prediction':round(prediction[0][0],2)})

@app.route("/resultados", methods=['POST'])
def resultados():
	marca=request.form.get("brand")
	modelo=request.form.get("model")
	combustible=request.form.get("fuel")
	results=db.session.query(Offer).filter(and_(Offer.brand==marca, Offer.model==modelo, Offer.fuel==combustible)).all()
	return render_template("resultados.html", results=results, marca=marca, modelo=modelo, combustible=combustible)

if __name__=="__main__":
	with app.app_context():
		main()