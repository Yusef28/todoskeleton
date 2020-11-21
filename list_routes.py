#!interpreter [optional-arg]
# -*- coding: utf-8 -*-

"""
list_routes.py

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


@app.route("/list_create", methods=('GET', 'POST'))
def list_create():

	if request.method == 'POST':
		list = List(title=request.form['new_list'], parent_user=session['user_id'])
		db.session.add(list)
		db.session.commit()

		print('List *'+list.title+'* for user with id: *'+str(session['user_id'])+'* created!')
		flash('List *'+list.title+'* for user with id: *'+str(session['user_id'])+'* created!')
	
	return redirect(url_for('dashboard'))
	
	
@app.route("/liste_lesen")
def liste_lesen(id):
	listen = List.query.filter_by(parent_user=id)
	for liste in listen:
		print(liste.title)
	return 'Listen gelesen'

	
@app.route("/liste_update")
def liste_update(id, neue):
	list = db.session.query(List).get(id)
	alt = list.title
	list.title = neue
	db.session.commit()
	print('Liste title von !'+alt+'! nach *'+list.title+'* Verandert!')
	return redirect(url_for('dashboard'))

 
@app.route("/list_delete/<int:id>")
def list_delete(id):
	list = List.query.get(id)
	if list.title == "Default":
		print('You cannot delete the Default list!')
		return redirect(url_for('dashboard'))
		
	if list.current == True:
		default = List.query.filter_by(title = "Default").first()
		list.current = False
		default.current = True
		
	db.session.delete(list)
	db.session.commit()
	print('List *'+list.title+'* Deleted!')
	return redirect(url_for('dashboard'))

	
@app.route("/liste_tasks")
def liste_tasks(id):
	tasks = Task.query.filter_by(parent_list = id)
	for task in tasks:
		print(task.title)
	print('Listen gelesen')
	return redirect(url_for('dashboard'))

	
#find the list with current=True
@app.route("/find_current_list")
def find_current_list(lists):
	for list in lists:
		if list.current == True:
			return list
			
			
@app.route("/change_current_list/<int:old_list_id>/<int:new_list_id>/")
def change_current_list(old_list_id, new_list_id):

	new_list = db.session.query(List).get(new_list_id)
	
	if not new_list:
		print("List ID not available")
	elif new_list.id == old_list_id:
		print("You are already viewing this list")
	else:
		old_list = db.session.query(List).get(old_list_id)
		old_list.current, new_list.current = new_list.current, old_list.current
		db.session.commit()
	
	#user = user_read(session['user_id'])
	return redirect(url_for('dashboard'))
	
	