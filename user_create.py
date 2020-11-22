#!interpreter [optional-arg]
# -*- coding: utf-8 -*-

"""
user_create.py

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
from wtforms import StringField
from wtforms.validators import DataRequired

from werkzeug.security import check_password_hash, generate_password_hash

'''
class Registration_form(FlaskForm):
	username = StringField('username', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired(), Email()])
	password = PasswordField('password', validators=[DataRequired()])
	password2 = PasswordField('password2', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('register')
'''


@app.route("/user_create")
def user_create(name, email, password):

	user = User(name=name, email=email, password=password)
	db.session.add(user)
	db.session.commit()
	#Init Default List
	'''
	default = List(title="Default", current = , parent_user=user.id)
	db.session.add(default)
	db.session.commit()
	
	task = Task(title="First Task", parent_list=default.id)
	db.session.add(task)
	task = Task(title="Second Task", parent_list=default.id)
	db.session.add(task)
	task = Task(title="Third Task Task", parent_list=default.id)
	db.session.add(task)
	db.session.commit()
	'''
	
	#Init Getting Started List
	getting_started_list = List(title="Getting Started", current = True, parent_user=user.id)
	db.session.add(getting_started_list)
	db.session.commit()
	
	task = Task(title="Try marking this task as completed!", parent_list=getting_started_list.id)
	db.session.add(task)
	task = Task(title="Try adding a new task!", parent_list=getting_started_list.id)
	db.session.add(task)
	task = Task(title="Try Creating a New List.", parent_list=getting_started_list.id)
	db.session.add(task)
	task = Task(title="Try adding a new task to the list", parent_list=getting_started_list.id)
	db.session.add(task)
	task = Task(title="Try deleting a task from a list", parent_list=getting_started_list.id)
	db.session.add(task)
	task = Task(title="Try restoring a task from the deleted filter", parent_list=getting_started_list.id)
	db.session.add(task)
	task = Task(title="Try completing a task and staring a task", parent_list=getting_started_list.id)
	db.session.add(task)
	task = Task(title="Try out the filters", parent_list=getting_started_list.id)
	db.session.add(task)
	db.session.commit()
	
	#Init Books to read List
	good_books_list = List(title="Good Books", current = False, parent_user=user.id)
	db.session.add(good_books_list)
	db.session.commit()
	
	task = Task(title="1984 By George Orwell", parent_list=good_books_list.id)
	db.session.add(task)
	task = Task(title="Anna Karenina By Leo Tolstoi", parent_list=good_books_list.id)
	db.session.add(task)
	task = Task(title="The Great Gatsby By F. Scott Fitzgerald", parent_list=good_books_list.id)
	db.session.add(task)
	task = Task(title="Alice in Wonderland By Lewis Carroll", parent_list=good_books_list.id)
	db.session.add(task)
	task = Task(title="A Clockwork Orange By Anthony Burgess", parent_list=good_books_list.id)
	db.session.add(task)
	
	db.session.commit()
	#Init Shopping List
	shopping_list = List(title="Shopping List (Empty)", current = False, parent_user=user.id)
	db.session.add(shopping_list)
	
	#Init Bucket List
	bucket_list = List(title="Bucket List (Empty)", current = False, parent_user=user.id)
	db.session.add(bucket_list)
	
	db.session.commit()
	
	print('User *'+user.name+'* created!')
	return True
	




