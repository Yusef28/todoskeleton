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
		
		new_task = Task(title=title, parent_list=current_list.id, sort_value=current_list.current_count+1)
		current_list.all_count += 1
		current_list.current_count += 1
		
		db.session.add(new_task)
		db.session.commit()
	
		print('Task *'+new_task.title+'* for List *'+current_list.title+'* created!')
		flash('Task *'+new_task.title+'* for List *'+current_list.title+'* created!')
	return redirect(request.referrer)

@app.route("/task_update/<int:id>", methods=('GET', 'POST'))
def task_update(id):
	
	if request.method == 'POST':
		
		new_title = request.form['task_title_change_input']
		task = db.session.query(Task).get(id)
		old_title = task.title
		task.title = new_title
		db.session.commit()
		
		print('Task title from !'+old_title+'! to *'+task.title+'* changed!')
	return redirect(request.referrer)

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
		
		task_shift_sort_values_left(task.id)
		#must change to completed AFTER shift 
		#because the shift gets all state=current tasks
		task.state = "completed"
		current_list = List.query.filter_by(id=task.parent_list).first()
		current_list.current_count -= 1
	else:
		task.state = "current"
		current_list = List.query.filter_by(id=task.parent_list).first()
		task.sort_value=current_list.current_count+1
		current_list.current_count += 1
		
	db.session.commit()
	return  redirect(request.referrer)
	
@app.route("/task_shift_sort_values_left/<int:id>")
def task_shift_sort_values_left(id):
	task = db.session.query(Task).get(id)
	task_sort_value = task.sort_value
	current_list = db.session.query(List).get(task.parent_list)
	current_list_count = current_list.current_count
	
	#I update all tasks, even tasks in the deleted or completed folders
	all_tasks_list = list(Task.query.filter_by(parent_list=current_list.id, state="current"))
	all_tasks_list.sort(key=lambda x:x.sort_value)
	print(all_tasks_list)
	print(task_sort_value)
	print(current_list_count)
	for i in range(task_sort_value, current_list_count):
	#	print(i)
	#	print(all_tasks_list[i].sort_value)
		all_tasks_list[i].sort_value -= 1
	task.sort_value = 0
	
	db.session.commit()

	
@app.route("/task_delete/<int:id>")
def task_delete(id):
	task = db.session.query(Task).get(id)
	
	#Neue
	if task.state == "current":
		
		print('Task *'+task.title+'* moved to trash as '+str(task.state))
		task_shift_sort_values_left(task.id)
		task.state = "deleted"
		current_list = List.query.filter_by(id=task.parent_list).first()
		current_list.current_count -= 1
		
	elif task.state == "deleted" or task.state == "completed":
	
		#shift values first
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
	if task.state == "deleted":
		task.state = "current"
		current_list = List.query.filter_by(id=task.parent_list).first()
		task.sort_value=current_list.current_count+1
		current_list.current_count += 1
	#task.deleted = False
	db.session.commit()
	print('Task *'+task.title+'* restored!')
	print('Set task *'+task.title+'* delete to *'+str(task.state))
	
	return redirect(request.referrer)

	
#muss loschen sort_value bei erste loschen
@app.route("/task_sort_up/<int:id>")
def task_sort_up(id):
	task_right = db.session.query(Task).get(id)
	task_right_sort_value = task_right.sort_value
	print("task_right_sort_value:")
	print(task_right_sort_value)
	if task_right_sort_value > 1:
	
		task_left = db.session.query(Task).filter_by(
		parent_list=task_right.parent_list, 
		sort_value=task_right_sort_value - 1 ).first()
		
		task_left_sort_value = task_left.sort_value
		task_left.sort_value = task_right_sort_value
		task_right.sort_value = task_left_sort_value
		
		db.session.commit()
	return redirect(request.referrer)
	
@app.route("/task_sort_down/<int:id>")
def task_sort_down(id):
	task_left = db.session.query(Task).get(id)
	task_left_sort_value = task_left.sort_value
	parent_list = List.query.filter_by(id=task_left.parent_list).first()
	if task_left.sort_value < parent_list.current_count:
	
		task_right = db.session.query(Task).filter_by(
		parent_list=task_left.parent_list, 
		sort_value=task_left.sort_value + 1 ).first()
		
		task_right_sort_value = task_right.sort_value
		task_left.sort_value = task_right_sort_value
		task_right.sort_value = task_left_sort_value
		
		db.session.commit()
	return redirect(request.referrer)
