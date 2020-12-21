#!interpreter [optional-arg]
# -*- coding: utf-8 -*-
#
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
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

from werkzeug.security import check_password_hash, generate_password_hash


#Modules
from flask_app import db, app
from models import User, List, Task
from user_create import *


class Registration_form(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Confirm Password', validators=[DataRequired()])#<h1>Registration</h1>
	submit = SubmitField('register')

class Login_form(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('login')


	
@app.route("/registration_wtf", methods=('GET', 'POST'))
def registration_wtf():
	
	#besser weg https://stackoverflow.com/questions/13585663/flask-wtfform-flash-does-not-display-errors
	
	form = Registration_form()#if "GET", create form to send to template
	if form.validate_on_submit():

		name = form.username.data 
		password = form.password.data
		confirmation = form.password2.data
		email = form.email.data
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
			return render_template('auth/registration_wtf.html', form=form)

		result = user_create(name, email, generate_password_hash(password))
		
		if result:
			flash(result)
			print(result)
			return redirect(url_for('login_wtf'))
		

	return render_template('auth/registration_wtf.html', form=form)
	

#Login_wtf 
@app.route("/login_wtf", methods=('GET', 'POST'))
def login_wtf():

	form = Login_form()#if "GET", create form to send to template
	if form.validate_on_submit():

		name = form.username.data 
		password = form.password.data
		error = None
		
		user = User.query.filter_by(name = name).first()#first or else you get an iterator
		
		if not user:
			error = 'User not found.'
			print(error)
			flash(error)
		
		#not check_password_hash(user.password, password)
		elif not check_password_hash(user.password, password):
			error = 'User name or password False.'
			print(error)
			flash(error)
			
		if not error:
			session.clear()
			session['user_id'] = user.id
			#with just dashboard() I get an onscreen error Badrequest
			return redirect(url_for('dashboard'))
		
	return render_template('auth/login_wtf.html', form=form)
	
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
		
		

@app.route("/user_read")
def user_read(id):
	user = User.query.get(id)
	return user
	

#unused
@app.route("/user_update")
def user_update(id, new):

	benutzer = User.query.get(id)
	alt = benutzer.name
	benutzer.name = new
	db.session.commit()
	benutzer = User.query.get(id)
	return 'Benutzer name von !'+alt+'! nach *'+benutzer.name+'* Verandert!'


@app.route("/user_delete")
def user_delete():
	print(session['user_id'])
	user = User.query.get(session['user_id'])
	db.session.delete(user)
	db.session.commit()
	print('User deleted!')
	return redirect(url_for('logout'))
	


