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



#Modules
from flask_app import db, app
from models import User, List, Task


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class Update_List_form(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('register')
	
	

@app.route("/list_create", methods=('GET', 'POST'))
def list_create():

	if request.method == 'POST':
		if "Getting Started" == request.form['new_list']:
			print('A list with this name already exists')
			return redirect(url_for('dashboard'))
			
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

	
@app.route("/list_update/<int:id>", methods=('GET', 'POST'))
def list_update(id):
	
	if request.method == 'POST':
		if "Getting Started" == request.form['list-title-change-input']:
			print('A list with this name already exists')
			return redirect(url_for('dashboard'))
			
		new_title = request.form['list-title-change-input']
		list = db.session.query(List).get(id)
		old_title = list.title
		list.title = new_title
		db.session.commit()
		print('List title from !'+old_title+'! to *'+list.title+'* changed!')
	return redirect(url_for('dashboard'))

@app.route("/list_update_wtf/<int:id>", methods=('GET', 'POST'))
def list_update_wtf(id):
	
	form = Update_List_form()
	if form.validate_on_submit():
		
		if "Getting Started" == form.title.data:
			print('A list with this name already exists')
			return redirect(url_for('dashboard'), list_update_form=form)
			
		new_title = form.title.data
		list = db.session.query(List).get(id)
		old_title = list.title
		list.title = new_title
		db.session.commit()
		print('List title from !'+old_title+'! to *'+list.title+'* changed!')
	return redirect(url_for('dashboard_wtf'), list_update_form=form)
 
@app.route("/list_delete/<int:id>")
def list_delete(id):
	list = db.session.query(List).get(id)
	if list.title == "Getting Started":
		print('You cannot delete the Getting Started list!')
		return redirect(url_for('dashboard'))
		
	if list.current == True:
		#I needed to search using default as title AND session id otherwise I get the first default List which
		#could be from another user!
		default = db.session.query(List).filter_by(title = "Getting Started", parent_user = session['user_id']).first()
		print(default.title)
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
			print('gefunden')
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
	
	