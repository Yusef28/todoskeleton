#!interpreter [optional-arg]
# -*- coding: utf-8 -*-
#
"""
task_routes.py

"""

#Built-in/Generic
import datetime

#Libs
from flask import Flask, g, redirect, render_template, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
		Table, Column, Integer, String, MetaData, ForeignKey, Boolean
	)


#Modules
from flask_app import db, app
from models import User, List, Task

from list_routes import find_current_list #for task_create()

@app.route("/task_create", methods=('GET', 'POST'))
def task_create():
	
	if request.method == 'POST':
		lists = List.query.filter_by(parent_user = session['user_id'])
		#num_lists = len(list(lists))
		current_list = find_current_list(lists) #needs the list_routes module
		
		title = request.form['new_task']
		#new_task = Task(title=title, parent_list=current_list.id)
		
		new_task = Task(title=title, parent_list=current_list.id, sort_value=current_list.all_count+1)
		current_list.all_count += 1
		
		db.session.add(new_task)
		db.session.commit()
	
		print('Task *'+new_task.title+'* for List *'+current_list.title+'* created!')
		flash('Task *'+new_task.title+'* for List *'+current_list.title+'* created!')
	return redirect(url_for('dashboard'))
	

@app.route("/task_important/<int:id>")
def task_important(id):
	task = db.session.query(Task).get(id)
	task.important = 1 - 1*task.important
	db.session.commit()

	return  redirect(request.referrer)

@app.route("/task_completed/<int:id>")
def task_completed(id):
	task = db.session.query(Task).get(id)
	
	#Neue
	if task.state == "current":
		task.state = "completed"
	elif task.state == "current-deleted":
		task.state = "completed-deleted"
	elif task.state == "completed-deleted":
		task.state = "current-deleted"
	else:
		task.state = "current"
		
	db.session.commit()
	return  redirect(request.referrer)
	
@app.route("/task_delete/<int:id>")
def task_delete(id):
	task = db.session.query(Task).get(id)
	
	#Neue
	if task.state == "current":
		task.state = "current-deleted"
		print('Task *'+task.title+'* moved to trash as '+str(task.state))
		
	elif task.state == "completed":
		task.state = "completed-deleted"
		print('Task *'+task.title+'* moved to trash as '+str(task.state))
		
	elif task.state == "deleted":
		current_list = db.session.query(List).get(task.parent_list)
		current_list.all_count -= 1
		db.session.delete(task)
		print('Task *'+task.title+'* deleted permenantly!')
		
	db.session.commit()
	return redirect(request.referrer)

@app.route("/task_delete_undo/<int:id>")
def task_delete_undo(id):

	
		
	task = db.session.query(Task).get(id)
	
	#Neue
	if task.state == "current-deleted":
		task.state = "current"
	elif task.state == "completed-deleted":
		task.state = "completed"
	
	#task.deleted = False
	db.session.commit()
	print('Task *'+task.title+'* restored!')
	print('Set task *'+task.title+'* delete to *'+str(task.state))
	
	return  redirect(request.referrer)

