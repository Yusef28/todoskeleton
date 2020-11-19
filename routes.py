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
from tabulate import tabulate

#Modules
from app import db, app
from models import User, List, Task

@app.route("/")
def index():
	return 'Hello, World'


#User

#C
@app.route("/user_create")
def user_create(name, email, password):
	#>>>import routes
	#>>>routes.user_create() -> 'Hallo, Welt'
	user = User(name=name, email=email, password=password)
	db.session.add(user)
	db.session.commit()
	
	default = List(title="Default", parent_user=user.id)
	db.session.add(default)
	db.session.commit()
	
	task = Task(title="First Task", parent_list=default.id)
	db.session.add(task)
	db.session.commit()
	
	#get data from form and validate
	#if all is good, it will render the login form
	#else return to this url
	return 'User *'+user.name+'* created!'
	
#R 
@app.route("/user_read")
def user_read(id):
	user = User.query.get(id)
	return 'User *'+user.name+'* read!'
	
#U
@app.route("/user_update")
def user_update(id, neue):
	#user = db.session.query(User).get(id)
	#user = User.query.filter_by(parent_user = id)
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
	listen = List.query.filter_by(parent_user = id)
	for liste in listen:
		print(liste.title)
	return 'Listen gelesen'
	

#List

#C
@app.route("/liste_erstellen")
def liste_erstellen(title, id):

	benutzer = User.query.get(id)
	liste = List(title=title, parent_user=id)
	db.session.add(liste)
	db.session.commit()

	return 'Liste *'+liste.title+'* fur benutzer *'+benutzer.name+'* erstellt!'
	
#R 
@app.route("/liste_lesen")
def liste_lesen(id):
	listen = List.query.filter_by(parent_user=id)
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
	tasks = Task.query.filter_by(parent_list = id)
	for task in tasks:
		print(task.title)
	return 'Listen gelesen'


#Task

#C
@app.route("/task_erstellen")
def task_erstellen(title, id):

	list = List.query.get(id)
	task = Task(title=title, parent_list=id)
	db.session.add(task)
	db.session.commit()
	
	return 'Task *'+task.title+'* fur List *'+list.title+'* erstellt!'
	
#R 
@app.route("/task_lesen")
def task_lesen(id):
	#list id hier
	tasks = Task.query.filter_by(parent_list=id)
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
		#start session?
		#frag nach all listen und tasks
		return zeige(user)
		

	return login()

#Diese funktioniert als ein schiene HTML Datei
@app.route("/zeige")
def zeige(user):
	print(f"Hallo wieder {user.name}")
	print("Was wollen sie heute Nacht tun?")
	print("hier sind seinem listen...")
	print("")
	#listen = List.query.filter(parent_user=user.id)
	listen = List.query.filter_by(parent_user = user.id)
	
	#list von listen
	listen_text = []
	for l in listen:
		listen_text += [f"{l.id} {l.title}"]
	
	#liste von aufgaben fur die erste liste (spater die aktuelle liste)
	aktuelle_liste = []
	if listen_text:
		tasks = Task.query.filter_by(parent_list=listen[0].id)
		aktuelle_liste = [i.title for i in tasks]
	listen_text = ["D:Default", "I:Important", "C:Completed", "L:Deleted","--------"] + listen_text
	
	optionen = ['1: List Create', 
				'2: List Edit',
				'3: List Delete',
				'4: List Read',
				'--------------',
				'5: New Task', 
				'6: Task Complete',
				'7: Task Delete',
				'8: Task Important',
				'9: Log-out']
				
	#padding
	ma = max(len(aktuelle_liste), len(listen_text), len(optionen))
	for x in [listen_text, aktuelle_liste, optionen]:
		x += [""]*(ma - len(x))

	#erstelle ein tabelle und druck
	table = [[x,y,z] for x,y,z in zip(listen_text, aktuelle_liste, optionen)]
	headers = ["Listen", "Aufgaben", "optionen"]
	print(tabulate(table, headers, tablefmt="pretty"))
	print("")
		
	antwort = input()
	
	#Neue List Erstellen
	if antwort == '1':
		print('geben sie ein title ein')
		title = input()
		liste_erstellen(title, user.id)
		return zeige(user)
		
	#List Bearbeiten
	elif antwort == '2':
		
		return zeige(user)
		
	#List Loschen
	elif antwort == '3':
		
		return zeige(user)
	#List Lesen
	elif antwort == '4':
		
		return zeige(user)
	
	#Neue Aufgabe (Fur aktuelle liste) (oder auch list id hinzufugen?)
	elif antwort == '5':
		
		return zeige(user)
	
	#Aufgabe Fertig
	elif antwort == '6':
		
		return zeige(user)
	
	#aufgabe Loschen
	elif antwort == '7':
		
		return zeige(user)
	
	#zeig als Wichtig
	elif antwort == '8':
		
		return zeige(user)
	
	#Ausloggen
	elif antwort == '9':
		print('du bist ausgelogged')
		return 

		
	return zeige(user)

#Logout
@app.route("/logout")
def logout(id):
	pass