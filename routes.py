#!interpreter [optional-arg]
# -*- coding: utf-8 -*-
#
"""
routes.py: All Routes 

"""

#Built-in/Generic
import datetime

#Libs
from flask import Flask, g, redirect, render_template, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
		Table, Column, Integer, String, MetaData, ForeignKey, Boolean
	)
from sqlalchemy import or_

#Modules
from flask_app import db, app
from models import User, List, Task
import task_routes, \
	list_routes, \
	user_routes, \
	task_time_routes, \
	task_advanced_form
	
#for some reason I need to also import all from each of these. 
#especially list_routes for find all from list
from list_routes import *
from task_routes import *
from user_routes import *
from task_time_routes import *
from task_advanced_form import *


@app.route("/get_lists_and_current_list")
def get_lists_and_current_list():
	user = user_read(session['user_id'])
	lists = List.query.filter_by(parent_user = user.id)
	current_list = find_current_list(lists)
	return lists, current_list
	
	
@app.route("/")
def index():
	num_users = db.session.query(User).count()
	num_lists = db.session.query(List).count()
	num_tasks = db.session.query(Task).count()
	if 'user_id' not in session or not user_read(session['user_id']):
	#on start and after clear
		return render_template('auth/index.html', num_users=num_users, num_lists=num_lists, num_tasks=num_tasks)
	else:
		lists, current_list = get_lists_and_current_list()
		return render_template('auth/index.html', lists=lists, current_list=current_list, 
		num_users=num_users, num_lists=num_lists, num_tasks=num_tasks)
		
		
@app.route("/filter_current")
def filter_current():
	lists, current_list = get_lists_and_current_list()
	if not current_list:
		return render_template('list/dashboard.html', lists=lists, current_list = current_list)
	current_tasks = Task.query.filter_by(parent_list=current_list.id, state="current")
	current_tasks = sorted(list(current_tasks), key=lambda x:(-x.important, x.sort_value))
	return render_template('list/dashboard.html', lists = lists, tasks = current_tasks, current_list = current_list, filter="current")
	
	
@app.route("/filter_important")
def filter_important():
	lists, current_list = get_lists_and_current_list()
	if not current_list:
		return render_template('list/dashboard.html', lists=lists, current_list = current_list)
	current_tasks = Task.query.filter_by(parent_list=current_list.id, 
	important=True).filter(or_(Task.state=="current", Task.state=="completed"))
	
	return render_template('list/dashboard.html', lists = lists, tasks = current_tasks, current_list = current_list, filter="Important")
	

@app.route("/filter_completed")
def filter_completed():
	lists, current_list = get_lists_and_current_list()
	if not current_list:
		return render_template('list/dashboard.html', lists=lists, current_list = current_list)
	current_tasks = Task.query.filter_by(parent_list=current_list.id, state="completed")
	return render_template('list/dashboard.html', lists = lists, tasks = current_tasks, current_list = current_list, filter="Completed")
	
	
@app.route("/filter_deleted")
def filter_deleted():
	lists, current_list = get_lists_and_current_list()
	if not current_list:
		return render_template('list/dashboard.html', lists=lists, current_list = current_list)
	current_tasks = Task.query.filter_by(
	parent_list=current_list.id, ).filter(or_(Task.state=="current-deleted", Task.state=="deleted"))
	#http://www.leeladharan.com/sqlalchemy-query-with-or-and-like-common-filters
	
	return render_template('list/dashboard.html', lists = lists, tasks = current_tasks, current_list = current_list, filter="Deleted")
	
	
@app.route("/dashboard_show_lists")
def dashboard_show_lists():
	#get all lists and tasks for that list
	
	lists, current_list = get_lists_and_current_list()
	
	#if you're here, there is no current list
	if current_list:
		current_list.current = False
		db.session.commit()
	return render_template('list/dashboard_lists.html', lists=lists)
	
	
@app.route("/dashboard")
def dashboard():
	
	#get all lists and tasks for that list
	lists, current_list = get_lists_and_current_list()
	
	if not current_list:
		return render_template('list/dashboard_lists.html', lists=lists)
	
	current, completed, deleted = [], [], []
	tasks = Task.query.filter_by(parent_list=current_list.id)
	tasks = sorted(list(tasks), key=lambda x:(
	-x.important,
	x.state=="deleted",
	x.state=="current",
	x.state=="completed",
	x.id))
	
	for task in tasks:
		if task.state == "current":
			current.append(task)
		elif task.state == "completed":
			completed.append(task)
		else:
			deleted.append(task)
			
	current = sorted(current, key=lambda x:(-x.important, x.sort_value))
	
	return render_template('list/dashboard_filter_all.html', 
	lists = lists, 
	tasks = tasks, 
	deleted=deleted, 
	completed=completed, 
	current=current, 
	current_list=current_list, 
	filter="All")
	
