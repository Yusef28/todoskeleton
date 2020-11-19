#!interpreter [optional-arg]
# -*- coding: utf-8 -*-


"""
app.py: Erstellt und konfiguriert die Flask Anwendung
Erstellt ein SQLAlchemy database
Importiert Routes fur verwendung
Importiert Modelen fur CLI init

Fur cli init:
C:/path>py
>>>from app import db
>>>db.create_all()
mit flask-sqlalchmemy gibt es keine "from Base import Session"
Stattdessen haben wir db.create_all()

>>>dann import alle modelln und dann 
>>>db.session.add(...)
>>>db.session.add(...)
>>>db.session.commit()

Und dann 
>>>u = User.query.all()
>>>print(u) oder u

Wenn ein table existiert nicht, sie muss die uri auf ein
nummer hoher (zbs test4 -> test5 ->test 6)
und die ganze erneue versuchen

>>> u = User.query.all()
>>> for i in u:print(i.name)
>>> l = List.query.all()
>>> for i in l:print(i.title)
>>> t = Task.query.all()
>>> for i in t:print(i.title)


und spater
db.session.add(Task(title="aufgabe 3", eltern_list=l[0].id))
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test11.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Modules
import routes
from models import User, List, Task


