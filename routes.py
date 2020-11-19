#!interpreter [optional-arg]
# -*- coding: utf-8 -*-

"""
routes.py: Alle Routes 

"""

#Built-in/Generic
import datetime

#Libs
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
		Table, Column, Integer, String, MetaData, ForeignKey, Boolean
	)

#Modules
from app import db, app
from models import User, List, Task

@app.route("/")
def index():
	return 'Hallo, Welt'


#User

#C
@app.route("/benutzer_erstellen")
def benutzer_erstellen(name):
	#>>>import routes
	#>>>routes.benutzer_erstellen() -> 'Hallo, Welt'
	benutzer = User(name=name)
	db.session.add(benutzer)
	db.session.commit()
	
	default = List(title="Default", eltern_user=benutzer.id)
	db.session.add(default)
	db.session.commit()
	
	task = Task(title="fang an", eltern_list=default.id)
	db.session.add(task)
	db.session.commit()
	return 'Benutzer *'+benutzer.name+'* erstellt!'
	
#R 
@app.route("/benutzer_lesen")
def benutzer_lesen(id):
	benutzer = User.query.get(id)
	return 'Benutzer *'+benutzer.name+'* Gelesen!'
	
#U
@app.route("/benutzer_aktualizieren")
def benutzer_aktualizieren(id, neue):
	#benutzer = db.session.query(User).get(id)
	#benutzer = User.query.filter_by(eltern_user = id)
	benutzer = User.query.get(id)
	alt = benutzer.name
	benutzer.name = neue
	#db.session.add(benutzer)
	db.session.commit()
	benutzer = User.query.get(id)
	return 'Benutzer name von !'+alt+'! nach *'+benutzer.name+'* Verandert!'

#D 
@app.route("/benutzer_loschen")
def benutzer_loschen(id):
	benutzer = User.query.get(id)
	db.session.delete(benutzer)
	db.session.commit()
	return 'Benutzer geloscht!'

@app.route("/benutzer_listen")
def benutzer_listen(id):
	listen = List.query.filter_by(eltern_user = id)
	for liste in listen:
		print(liste.title)
	return 'Listen gelesen'
	

#List

#C
@app.route("/liste_erstellen")
def liste_erstellen(title, id):

	liste = List(title=title, eltern_user=id)
	db.session.add(liste)
	db.session.commit()

	return 'Liste *'+liste.title+'* erstellt!'
#R 
@app.route("/liste_lesen")
def liste_lesen(id):
	pass
	#tasks = List.query.get(id)
	#return 'Benutzer *'+benutzer.name+'* Gelesen!'
#U
@app.route("/liste_aktualizieren")
def liste_aktualizieren(id, neue):
	list = db.session.query(List).get(id)
	alt = list.title
	list.title = neue
	db.session.commit()
	return 'Liste title von !'+alt+'! nach *'+list.title+'* Verandert!'
#D 
@app.route("/liste_loschen")
def liste_loschen(id):
	list = List.query.get(id)
	db.session.delete(list)
	db.session.commit()
	return 'List geloscht!'

@app.route("/liste_tasks")
def liste_tasks(id):
	tasks = Task.query.filter_by(eltern_list = id)
	for task in tasks:
		print(task.title)
	return 'Listen gelesen'


#Task

#C

#R 

#U

#D 



	

