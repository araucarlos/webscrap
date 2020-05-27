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

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://postgres:mejor2@localhost:5432/autocasion?client_encoding=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
db.init_app(app)

def main():
	db.create_all()

if __name__=="__main__":
	with app.app_context():
		main()