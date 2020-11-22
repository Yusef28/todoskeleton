#!interpreter [optional-arg]
# -*- coding: utf-8 -*-

"""
user_routes.py

"""

#Built-in/Generic
import datetime

#Libs
from flask import Flask, g, redirect, render_template, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
		Table, Column, Integer, String, MetaData, ForeignKey, Boolean
	)
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from werkzeug.security import check_password_hash, generate_password_hash


#Modules
from flask_app import db, app
from models import User, List, Task
from user_create import *
'''
class Registration_form(FlaskForm):
	username = StringField('username', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired(), Email()])
	password = PasswordField('password', validators=[DataRequired()])
	password2 = PasswordField('password2', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('register')
'''

@app.route("/registration", methods=('GET', 'POST'))
def registration():
	
	#form = Registration_form()
	#{{ form.csrf_token }}
	#{{ form.username.label }} {{ form.username(class='form-control', size=20) }}
	#print(form.validate_on_submit())
	#print(form.errors)
	
	
	if request.method == 'POST':
		name = request.form['username'] #form.username.data 
		password = request.form['password']
		confirmation = request.form['password2']
		email = request.form['email']
		error = None
		
		if User.query.filter_by(name = name).first():
			error = 'user name already registered.'
			flash(error)
			print(error)
			
		if User.query.filter_by(email = email).first():
			error = 'user email already registered.'
			flash(error)
			print(error)
		
		if len(password) < 8:
			error = 'password must be at least 8 characters long.'
			flash(error)
			print(error)
		
		if password != confirmation:
			error = 'password and confirmation password must match.'
			flash(error)
			print(error)
			
		if error:
			return render_template('auth/registration.html')
			#return render_template('auth/registration.html', form=form)
			
			#generate_password_hash(password)
		result =  user_create(name, email, password)
		
		if result:
			flash(result)
			print(result)
			return redirect(url_for('login'))
		

	return render_template('auth/registration.html')
	
#Login 
@app.route("/login", methods=('GET', 'POST'))
def login():

	if request.method == 'POST':
		name = request.form['username']
		password = request.form['password']		
		error = None
		user = User.query.filter_by(name = name).first()#first or else you get an iterator
		
		if not user:
			error = 'User not found.'
			print(error)
			flash(error)
		
		#not check_password_hash(user.password, password)
		elif user.password != password:
			error = 'User name or password False.'
			print(error)
			flash(error)
			
		if not error:
			session.clear()
			session['user_id'] = user.id
			#with just dashboard() I get an onscreen error Badrequest
			return redirect(url_for('dashboard'))
		
	return render_template('auth/login.html')

@app.route("/logout")
def logout():
	session.clear()
	return redirect(url_for('index'))
	
#This is cool (if calls the following function
#before every request. and there is a bp version.

@app.before_request
def load_logged_in_user():
	#I think I needed "get()" instead of just session['key']
	#for the case that session doesn't have a user_id yet?
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = user_read(user_id)
		
		

#User functions
'''
@app.route("/user_create")
def user_create(name, email, password):

	user = User(name=name, email=email, password=password)
	db.session.add(user)
	db.session.commit()
	
	default = List(title="Default", current = True, parent_user=user.id)
	db.session.add(default)
	db.session.commit()
	
	task = Task(title="First Task", parent_list=default.id)
	db.session.add(task)
	db.session.commit()
	
	print('User *'+user.name+'* created!')
	return True
'''

@app.route("/user_read")
def user_read(id):
	user = User.query.get(id)
	return user
	

#unused
@app.route("/user_update")
def user_update(id, neue):

	benutzer = User.query.get(id)
	alt = benutzer.name
	benutzer.name = neue
	db.session.commit()
	benutzer = User.query.get(id)
	return 'Benutzer name von !'+alt+'! nach *'+benutzer.name+'* Verandert!'


@app.route("/user_delete")
def user_delete():
	user = User.query.get(session['user_id'])
	db.session.delete(user)
	db.session.commit()
	print('User deleted!')
	return redirect(url_for('logout'))
	


