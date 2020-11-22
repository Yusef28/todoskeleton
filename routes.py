#!interpreter [optional-arg]
# -*- coding: utf-8 -*-

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
from tabulate import tabulate

#Modules
from flask_app import db, app
from models import User, List, Task
import task_routes, list_routes, user_routes
#for somereason I need to also import all from each of these. 
#especially list_routes for find all from list
from list_routes import *
from task_routes import *
from user_routes import *


@app.route("/")
def index():
	return render_template('auth/index.html')


@app.route("/dashboard_all_info")
def dashboard_all_info():
	pass


@app.route("/dashboard_current")
def dashboard_current():
	user = user_read(session['user_id'])
	lists = List.query.filter_by(parent_user = user.id)
	current_list = find_current_list(lists)
	current_tasks = Task.query.filter_by(parent_list=current_list.id, current=True, deleted=False)
	return render_template('list/dashboard.html', lists = lists, tasks = current_tasks, current_list = current_list)
	
	
@app.route("/dashboard_important")
def dashboard_important():
	user = user_read(session['user_id'])
	lists = List.query.filter_by(parent_user = user.id)
	current_list = find_current_list(lists)
	current_tasks = Task.query.filter_by(parent_list=current_list.id, important=True, deleted=False)
	return render_template('list/dashboard.html', lists = lists, tasks = current_tasks, current_list = current_list)
	

@app.route("/dashboard_completed")
def dashboard_completed():
	user = user_read(session['user_id'])
	lists = List.query.filter_by(parent_user = user.id)
	current_list = find_current_list(lists)
	current_tasks = Task.query.filter_by(parent_list=current_list.id, completed=True, deleted=False)
	return render_template('list/dashboard.html', lists = lists, tasks = current_tasks, current_list = current_list)
	
	
@app.route("/dashboard_deleted")
def dashboard_deleted():
	user = user_read(session['user_id'])
	lists = List.query.filter_by(parent_user = user.id)
	current_list = find_current_list(lists)
	current_tasks = Task.query.filter_by(parent_list=current_list.id, deleted=True)
	return render_template('list/dashboard.html', lists = lists, tasks = current_tasks, current_list = current_list)
	


@app.route("/dashboard")
def dashboard():

	#get all lists and tasks for that list
	user = user_read(session['user_id'])
	lists = db.session.query(List).filter_by(parent_user = user.id)
	current_list = find_current_list(lists)
	tasks = Task.query.filter_by(parent_list=current_list.id, deleted=False)

	#return dashboard(user)
	return render_template('list/dashboard.html', lists = lists, tasks = tasks, current_list = current_list)
	
