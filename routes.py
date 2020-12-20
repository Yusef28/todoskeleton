#!interpreter [optional-arg]
# -*- coding: utf-8 -*-
#
"""
routes.py: Alle Routes 

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
import task_routes, list_routes, user_routes
#for somereason I need to also import all from each of these. 
#especially list_routes for find all from list
from list_routes import *
from task_routes import *
from user_routes import *



@app.route("/get_lists_and_current_list")
def get_lists_and_current_list():
	user = user_read(session['user_id'])
	lists = List.query.filter_by(parent_user = user.id)
	current_list = find_current_list(lists)
	return lists, current_list
	
	
@app.route("/")
def index():
	if 'user_id' not in session or not user_read(session['user_id']):
	#on start and after clear
		return render_template('auth/index.html')
	else:
		lists, current_list = get_lists_and_current_list()
		return render_template('auth/index.html', lists=lists, current_list=current_list)
		
		
@app.route("/dashboard_current")
def dashboard_current():
	lists, current_list = get_lists_and_current_list()
	if not current_list:
		return render_template('list/dashboard.html', lists=lists, current_list = current_list)
	current_tasks = Task.query.filter_by(parent_list=current_list.id, current=True, deleted=False)
	current_tasks = sorted(list(current_tasks), key=lambda x:(-x.important, x.id))
	return render_template('list/dashboard.html', lists = lists, tasks = current_tasks, current_list = current_list)
	
	
@app.route("/dashboard_important")
def dashboard_important():
	lists, current_list = get_lists_and_current_list()
	if not current_list:
		return render_template('list/dashboard.html', lists=lists, current_list = current_list)
	current_tasks = Task.query.filter_by(parent_list=current_list.id, important=True, deleted=False)
	return render_template('list/dashboard.html', lists = lists, tasks = current_tasks, current_list = current_list)
	

@app.route("/dashboard_completed")
def dashboard_completed():
	lists, current_list = get_lists_and_current_list()
	if not current_list:
		return render_template('list/dashboard.html', lists=lists, current_list = current_list)
	current_tasks = Task.query.filter_by(parent_list=current_list.id, completed=True, deleted=False)
	return render_template('list/dashboard.html', lists = lists, tasks = current_tasks, current_list = current_list)
	
	
@app.route("/dashboard_deleted")
def dashboard_deleted():
	lists, current_list = get_lists_and_current_list()
	if not current_list:
		return render_template('list/dashboard.html', lists=lists, current_list = current_list)
	current_tasks = Task.query.filter_by(parent_list=current_list.id, deleted=True)
	return render_template('list/dashboard.html', lists = lists, tasks = current_tasks, current_list = current_list)
	
	
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
		
	tasks = Task.query.filter_by(parent_list=current_list.id, deleted=False)
	tasks = sorted(list(tasks), key=lambda x:(-x.important, x.id))
	return render_template('list/dashboard.html', lists = lists, tasks = tasks, current_list = current_list)
	
