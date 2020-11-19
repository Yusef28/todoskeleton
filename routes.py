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
def benutzer_erstellen(name, email, password):
	#>>>import routes
	#>>>routes.benutzer_erstellen() -> 'Hallo, Welt'
	benutzer = User(name=name, email=email, password=password)
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

	benutzer = User.query.get(id)
	liste = List(title=title, eltern_user=id)
	db.session.add(liste)
	db.session.commit()

	return 'Liste *'+liste.title+'* fur benutzer *'+benutzer.name+'* erstellt!'
	
#R 
@app.route("/liste_lesen")
def liste_lesen(id):
	listen = List.query.filter_by(eltern_user=id)
	for liste in listen:
		print(liste.title)
	return 'Listen gelesen'
	#pass
	#tasks = List.query.get(id)
	#return 'Benutzer *'+benutzer.name+'* Gelesen!'
	
#U
#krieg die liste VON ein benutzer und verandern die name
#Die benutzer halt die id's fur seinem listen also ich muss nur
#ein list id eingeben, ich hoffe
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
	return 'List *'+list.title+'* geloscht!'

@app.route("/liste_tasks")
def liste_tasks(id):
	tasks = Task.query.filter_by(eltern_list = id)
	for task in tasks:
		print(task.title)
	return 'Listen gelesen'


#Task

#C
@app.route("/task_erstellen")
def task_erstellen(title, id):

	list = List.query.get(id)
	task = Task(title=title, eltern_list=id)
	db.session.add(task)
	db.session.commit()
	
	return 'Task *'+task.title+'* fur List *'+list.title+'* erstellt!'
	
#R 
@app.route("/task_lesen")
def task_lesen(id):
	#list id hier
	tasks = Task.query.filter_by(eltern_list=id)
	for task in tasks:
		print(task.title)
	return 'Tasks gelesen'

	
#U
@app.route("/task_aktualizieren")
def task_aktualizieren(id, neue):
	#task id hier
	task = db.session.query(Task).get(id)
	alt = task.title
	task.title = neue
	db.session.commit()
	return 'task title von !'+alt+'! nach *'+task.title+'* Verandert!'

#D 
@app.route("/task_loschen")
def task_loschen(id):
	task = Task.query.get(id)
	db.session.delete(task)
	db.session.commit()
	return 'List *'+task.title+'* geloscht!'


#Login
@app.route("/login")
def login():

	print("Geben sie ein Benutzer Name ein...")
	name = input()
	print("Geben sie ein Kenntwort ein...")
	kenntwort = input()
	
	if not name:
		error = 'Benutzername ist notig.'
		print(error)
		
	elif not kenntwort:
		error = 'Kenntwort ist notig.'
		print(error)
		
	user = User.query.filter_by(name = name).first()#first weil anderfalls sie krieg ein increment objekt
	print(user)
	
	
	if not user:
		error = 'Benutzer nicht vorhanden'
		print(error)
		
	elif user.password != kenntwort:
		error = 'Benutzername oder Kenntwort ist falsch'
		print(error)
		
	else:
		return zeige(user)
		
	db.session.delete(task)
	db.session.commit()
	return task_loschen()

@app.route("/zeige")
def zeige(user):
	print(f"Hallo wieder {user.name}")
	print("Was wollen sie heute Nacht tun?")
	print("hier sind seinem listen...")
	#listen = List.query.filter(eltern_user=user.id)
	listen = List.query.filter_by(eltern_user = user.id)
	for l in listen:
		print(f"{l.id}: {l.title}")
		
	print("oder vielleicht mochten Sie einfach ausloggen? Y/y:N/n")
	antwort = input()
	
	if antwort in ['Y','y']:
		print('du bist ausgelogged')
		return 

		
	return zeige()

#Logout
@app.route("/logout")
def logout(id):
	#task = Task.query.get(id)
	#db.session.delete(task)
	#db.session.commit()
	#return
	pass

	


