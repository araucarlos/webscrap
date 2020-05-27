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

app=Flask(__name__)

engine=create_engine('postgresql://postgres:mejor2@localhost:5432/autocasion')
db=scoped_session(sessionmaker(bind=engine))

@app.route("/", methods=["GET","POST"])
def index():
	marcas=db.execute("SELECT DISTINCT marca FROM autocasion").fetchall()
	modelos=db.execute("SELECT DISTINCT modelo FROM autocasion").fetchall()
	combustible=db.execute("SELECT DISTINCT combustible FROM autocasion").fetchall()
	return render_template("index.html", marcas=marcas, modelos=modelos, combustible=combustible)

@app.route("/resultados", methods=['POST'])
def resultados():
	marca=request.form.get("marca")
	modelo=request.form.get("modelo")
	combustible=request.form.get("combustible")
	results=db.execute("SELECT * FROM autocasion WHERE marca=:marca AND modelo=:modelo AND combustible=:combustible", {"marca":marca, "modelo":modelo, "combustible":combustible}).fetchall()
	return render_template("resultados.html", results=results, marca=marca, modelo=modelo, combustible=combustible)