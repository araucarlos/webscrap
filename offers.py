#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 13:09:17 2020

@author: carlosarau
"""

import os
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Offer(db.Model):
	__tablename__ = "offers"
	id=db.Column(db.Integer,primary_key=True)
	vehicle=db.Column(db.String,nullable=False)
	brand=db.Column(db.String,nullable=False)
	model=db.Column(db.String,nullable=False)
	grade=db.Column(db.String)
	drive=db.Column(db.String,nullable=False)
	price=db.Column(db.Numeric,nullable=False)
	registration_date=db.Column(db.Date,nullable=False)
	fuel=db.Column(db.String,nullable=False)
	mileage=db.Column(db.Numeric,nullable=False)
	body_type=db.Column(db.String)
	transmission=db.Column(db.String,nullable=False)
	horse_power=db.Column(db.Numeric)
	warranty=db.Column(db.Numeric,nullable=False)
	eco_label=db.Column(db.String)
	months=db.Column(db.Integer,nullable=False)
