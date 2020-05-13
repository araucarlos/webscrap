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

@app.route("/")
def index():
    results=db.execute("SELECT * FROM autocasion").fetchall()
    return render_template("index.html",results=results)
