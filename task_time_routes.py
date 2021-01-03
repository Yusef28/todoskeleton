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

#https://www.journaldev.com/23365/python-string-to-datetime-strptime

@app.route("/task_start_date_time_update/<int:id>", methods=('GET', 'POST'))
def task_start_date_time_update(id):
	
	if request.method == 'POST':
		
		start_date = request.form['task_start_date']
		task = db.session.query(Task).get(id)
		old_start_date = task.start_date

		datetime_start_date = datetime.datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
		task.start_date = datetime_start_date
		db.session.commit()
		
	return redirect(request.referrer)

@app.route("/task_end_date_time_update/<int:id>", methods=('GET', 'POST'))
def task_end_date_time_update(id):
	
	if request.method == 'POST':
		
		end_date = request.form['task_end_date']
		task = db.session.query(Task).get(id)
		old_end_date = task.end_date

		datetime_end_date = datetime.datetime.strptime(end_date, '%Y-%m-%dT%H:%M')
		task.end_date = datetime_end_date
		db.session.commit()

	return redirect(request.referrer)

