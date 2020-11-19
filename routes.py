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
	'''
	print("Home")
	print("Welcome to the DuMi app")
	print("Enter 1 for Registration")
	print("Enter 2 for Login")
	print("Enter 3 to quit")

	print("")
	answer = input()
	if answer == "1":
		return redirect(url_for('registration'))
	elif answer == "2":
		return redirect(url_for('login'))
	'''

	return render_template('auth/index.html')

@app.route("/registration", methods=('GET', 'POST'))
def registration():
	print("Registration")
	print("")
	
	'''
	print("Enter a User Name")
	name = input()
	print("Enter an email")
	email = input()
	print("Enter an password")
	password = input()
	print("")
	'''
	
	if request.method == 'POST':
		name = request.form['benutzername']
		password = request.form['kenntwort']
		email = request.form['email']
		#if the user creation works, go to login
		result =  user_create(name, email, password)
		
		if result:
			print(result)
			print("")
			return redirect(url_for('login'))
		
	#print('invalid registration')
	#return registration()
	return render_template('auth/registration.html')
	
#User

#C
@app.route("/user_create")
def user_create(name, email, password):
	#>>>import routes
	#>>>routes.user_create() -> 'Hallo, Welt'
	user = User(name=name, email=email, password=password)
	db.session.add(user)
	db.session.commit()
	
	default = List(title="Default", current = True, parent_user=user.id)
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
@app.route("/list_delete")
def list_delete(id):
	list = List.query.get(id)
	if list.title == "Default":
		return 'You cannot delete the Default list!'
		
	if list.current == True:
		default = List.query.filter_by(title = "Default").first()
		list.current = False
		default.current = True
		
	db.session.delete(list)
	db.session.commit()
	return 'List *'+list.title+'* Deleted!'

@app.route("/liste_tasks")
def liste_tasks(id):
	tasks = Task.query.filter_by(parent_list = id)
	for task in tasks:
		print(task.title)
	return 'Listen gelesen'

#find the list with current=True
def find_current_list(lists):
	for list in lists:
		if list.current == True:
			return list

def change_current_list(old_list):

	print('enter id for new list')
	new_list_id = input()
	
	new_list = db.session.query(List).get(new_list_id)
	
	if not new_list:
		return print("List ID not available")
	elif new_list.id == old_list.id:
		return print("You are already viewing this list")

	old_list = db.session.query(List).get(old_list.id)
	
	
	old_list.current, new_list.current = new_list.current, old_list.current
	db.session.commit()
	return print('Current list changed!')
	
	
			
#Task

#C
@app.route("/task_create")
def task_create(title, id):
	
	list = List.query.get(id)
	task = Task(title=title, parent_list=id)
	db.session.add(task)
	db.session.commit()
	
	return 'Task *'+task.title+'* for List *'+list.title+'* created!'
	
#R 
#@app.route("/task_lesen")
#def task_lesen(id):
#	#list id hier
#	tasks = Task.query.filter_by(parent_list=id)
#	for task in tasks:
#		print(task.title)
#	return 'Tasks gelesen'

#U
@app.route("/task_update")
def task_update(id, neue):
	#task id hier
	task = db.session.query(Task).get(id)
	old = task.title
	task.title = neue
	db.session.commit()
	return 'task title von !'+old+'! nach *'+task.title+'* updated!'

#D 
@app.route("/task_delete")
def task_delete(id):
	task = Task.query.get(id)
	db.session.delete(task)
	db.session.commit()
	return 'List *'+task.title+'* deleted!'


#Login 
@app.route("/login", methods=('GET', 'POST'))
def login():

	'''
	print("Login")
	print("Geben sie ein Benutzer Name ein...")
	name = input()
	print("Geben sie ein Kenntwort ein...")
	kenntwort = input()
	'''
	if request.method == 'POST':
		name = request.form['benutzername']
		password = request.form['kenntwort']
		
		error = None
		if not name:
			error = 'You need to enter a user name.'
			print(error)
			
		elif not password:
			error = 'You need to enter a password.'
			print(error)
			
		if error:
			return login()
			
		user = User.query.filter_by(name = name).first()#first weil anderfalls sie krieg ein increment objekt
		#print(user)
		
		
		if not user:
			error = 'User not found.'
			print(error)
			
		elif user.password != password:
			error = 'User name or password False.'
			print(error)
			
		else:
			#start session?
			#frag nach all listen und tasks
			return zeige(user)
		
	return render_template('auth/login.html')

#Diese funktioniert als ein schiene HTML Datei
@app.route("/zeige")
def zeige(user):
	print(f"Hallo wieder {user.name}")
	print("Was wollen sie heute Nacht tun?")
	print("hier sind seinem listen...")
	print("")
	#listen = List.query.filter(parent_user=user.id)
	listen = List.query.filter_by(parent_user = user.id)
	
	
	#for current list I have some options
	#1. make default un-deletable and if you delete current list, default becomes current list
	#2. if you delete current list, there is no current list and use must select one
	#3. if you have no lists and add one, it becomes the current list
	#4. if you have no lists and add one, you still have to select it
	#5. the app starts with a default list and it is current
	#6. the app starts with a default list but it is not current, you have to select it
	#7. you can select "Home" or some other option and then have no lists selected (so it's a state instead of an accident)
	
	#The easiest method (fewest lines of code) is just make default un deletable and 
	#if you delete the current list then default becomes current list(again). Catch the ball as it falls.
	
	current_list = find_current_list(listen)
	print(f"current list is {current_list.title}")
	
	#list of lists
	listen_text = []
	for l in listen:
		list_nav_title = f"{l.id}: {l.title}"
		if l.id == current_list.id:
			list_nav_title += "(A)"
		
		listen_text += [list_nav_title]
	
	#liste von aufgaben fur die erste liste (spater die aktuelle liste)
	current_tasks = []
	if listen_text:
		tasks = Task.query.filter_by(parent_list=current_list.id)
		current_tasks = [f"{i.id}: {i.title} I:{i.important}" for i in tasks]
	listen_text = ["D:Default", "I:Important", "C:Completed", "L:Deleted","--------"] + listen_text
	
	optionen = ['1: List Create', 
				'2: List Edit',
				'3: List Delete',
				'4: List Change',
				'--------------',
				'5: New Task', 
				'6: Task Complete',
				'7: Task Delete',
				'8: Task Important',
				'9: Log-out']
				
	#padding
	ma = max(len(current_tasks), len(listen_text), len(optionen))
	for x in [listen_text, current_tasks, optionen]:
		x += [""]*(ma - len(x))

	#erstelle ein tabelle und druck
	table = [[x,y,z] for x,y,z in zip(listen_text, current_tasks, optionen)]
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
		
	#List Delete
	elif antwort == '3':
		print('enter id for list to delete')
		delete_list_id = input()
		result = list_delete(delete_list_id)
		print(result)
		return zeige(user)
		
	#List Change
	elif antwort == '4':
		change_current_list(current_list)
		return zeige(user)
	
	#New task for current list
	elif antwort == '5':
		print("Enter the name of the task")
		title = input()
		result = task_create(title, current_list.id)  
		print(result)
		return zeige(user)
	
	#Task finish
	elif antwort == '6':
		#task_update(id, neue)
		return zeige(user)
	
	#Task Delete
	elif antwort == '7':
		print('enter the id for the task you want to delete')
		delete_task_id = input()
		result = task_delete(delete_task_id)
		print(result)
		return zeige(user)
	
	#zeig als Wichtig
	elif antwort == '8':
		
		return zeige(user)
	
	#Ausloggen
	elif antwort == '9':
		print('du bist ausgelogged')
		return index()

		
	return zeige(user)

#Logout
@app.route("/logout")
def logout(id):
	pass