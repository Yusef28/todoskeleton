#!interpreter [optional-arg]
# -*- coding: utf-8 -*-

#
"""
app.py: 
"""

#Built-in/Generic Imports
import datetime

#Libs
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
	Table, Column, Integer, String, MetaData, ForeignKey, Boolean
	)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test30.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'StArFox64'
db = SQLAlchemy(app)

#Modules
import routes
from models import User, List, Task


