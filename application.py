#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 13:09:17 2020

@author: carlosarau
"""

import os
from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from offers import *

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://postgres:mejor2@localhost:5432/autocasion"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
db.init_app(app)

@app.route("/", methods=["GET","POST"])
def index():
	marcas=db.session.query(Offer.brand).distinct()
	modelos=db.session.query(Offer.model).distinct()
	combustible=db.session.query(Offer.fuel).distinct()
	return render_template("index.html", marcas=marcas, modelos=modelos, combustible=combustible)

@app.route("/resultados", methods=['POST'])
def resultados():
	marca=request.form.get("marca")
	modelo=request.form.get("modelo")
	combustible=request.form.get("combustible")
	results=db.session.query(Offer).filter(and_(Offer.brand==marca, Offer.model==modelo, Offer.fuel==combustible)).all()
	return render_template("resultados.html", results=results, marca=marca, modelo=modelo, combustible=combustible)

if __name__=="__main__":
	with app.app_context():
		main()