#!interpreter [optional-arg]
# -*- coding: utf-8 -*-

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
from tabulate import tabulate

#Modules
from flask_app import db, app
from models import User, List, Task


@app.route("/task_create/<string:title>/<int:id>")
def task_create(title, id):
	
	list = List.query.get(id)
	task = Task(title=title, parent_list=id)
	db.session.add(task)
	db.session.commit()
	
	print('Task *'+task.title+'* for List *'+list.title+'* created!')
	#user = user_read(session['user_id'])
	return redirect(url_for('dashboard'))
	
@app.route("/task_update")
def task_update(id, neue):
	#task id hier
	task = db.session.query(Task).get(id)
	old = task.title
	task.title = neue
	db.session.commit()
	print('task title von !'+old+'! nach *'+task.title+'* updated!')
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

	#we only really need either current or completed
	task.current, task.completed = task.completed, task.current 
	db.session.commit()
	return  redirect(request.referrer)
	
@app.route("/task_delete/<int:id>")
def task_delete(id):
	task = db.session.query(Task).get(id)
	if task.deleted == False:
		task.deleted = True
		db.session.commit()
		print('Task *'+task.title+'* moved to trash!')
		print('Set task *'+task.title+'* delete to *'+str(task.deleted))
	elif task.deleted == True:
		db.session.delete(task)
		db.session.commit()
		print('Task *'+task.title+'* deleted permenantly!')
	return  redirect(request.referrer)

@app.route("/task_delete_undo/<int:id>")
def task_delete_undo(id):
	task = db.session.query(Task).get(id)
	task.deleted = False
	db.session.commit()
	print('Task *'+task.title+'* restored!')
	print('Set task *'+task.title+'* delete to *'+str(task.deleted))
	
	return  redirect(request.referrer)

