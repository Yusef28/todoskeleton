#!interpreter [optional-arg]
# -*- coding: utf-8 -*-
#
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
		
		title = request.form['new_list']
		if check_list_exists(title):
			flash('A list with this name already exists')
			return redirect(url_for('dashboard'))

		
		lists = db.session.query(List).filter_by(parent_user=session["user_id"]).all()
		old_current_list = find_current_list(lists)
		
		new_current_list = List(title=request.form['new_list'], parent_user=session['user_id'])
		
		#This needs to be here before the change/choose function calls 
		#because they query for this list and then update current
		db.session.add(new_current_list)
		db.session.commit()
		
		#when you create a new list, switch to immediately
		if old_current_list:
			change_current_list(old_current_list.id , new_current_list.id)
		else:
			choose_current_list(new_current_list.id)

		print('List *'+new_current_list.title+'* for user with id: *'+str(session['user_id'])+'* created!')
		flash('List *'+new_current_list.title+'* for user with id: *'+str(session['user_id'])+'* created!')
	
	return redirect(request.referrer)
	
@app.route("/list_update/<int:id>", methods=('GET', 'POST'))
def list_update(id):
	
	if request.method == 'POST':
		
		new_title = request.form['list_title_change_input']
		if check_list_exists(new_title):
			flash('A list with this name already exists')
			return redirect(url_for('dashboard'))

		list = db.session.query(List).get(id)
		old_title = list.title
		list.title = new_title
		db.session.commit()
		
		print('List title from !'+old_title+'! to *'+list.title+'* changed!')
	return redirect(url_for('dashboard'))

	
@app.route("/list_delete/<int:id>")
def list_delete(id):
	list = db.session.query(List).get(id)
	
	if list.current == True:
		list.current = False

	db.session.delete(list)
	db.session.commit()
	print('List *'+list.title+'* Deleted!')
	return redirect(url_for('dashboard'))

	
#find the list with current=True
@app.route("/find_current_list")
def find_current_list(lists):
	for list in lists:
		if list.current == True:
			return list
	return None
			
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
	
@app.route("/choose_current_list/<int:new_list_id>/")
def choose_current_list(new_list_id):

	new_list = db.session.query(List).get(new_list_id)
	
	if not new_list:
		print("List ID not available")
	else:
		new_list.current = True
		db.session.commit()
		
	return redirect(url_for('dashboard'))
	

@app.route("/check_list_exists/<string:title>/")
def check_list_exists(title):

	return db.session.query(List).filter_by(title=title, parent_user=session["user_id"]).first()
