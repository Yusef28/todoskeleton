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
from wtforms import (
		StringField, 
		PasswordField, 
		SubmitField, 
		DateTimeField,
		IntegerField,
		SelectField,
		TextAreaField
		)
from wtforms.validators import DataRequired, Email, EqualTo

from werkzeug.security import check_password_hash, generate_password_hash


#Modules
from flask_app import db, app
from models import User, List, Task
from user_create import *

class Advanced_Task_Creation_Form(FlaskForm):

	title = StringField('Title')
	
	start_date = DateTimeField('StartDate', 
	format="%Y-%m-%dT%H:%M")
	
	end_date = DateTimeField('EndDate', 
	format="%Y-%m-%dT%H:%M")
	
	reminder_date = DateTimeField('ReminderDate', 
	format="%Y-%m-%dT%H:%M")
	
	duration = IntegerField('Duration')
	recurrance = IntegerField('Recurrance')
	
	importance_rating = SelectField('ImportanceRating', 
	choices=[('0', '0'),
	('1', '1'),
	('2', '2'),
	('3', '3'),
	('4', '4'),
	('5', '5')])
	
	energy_rating = SelectField('EnergyRating', 
	choices=[('0', '0'),
	('1', '1'),
	('2', '2'),
	('3', '3'),
	('4', '4'),
	('5', '5'),
	('6', '6'),
	('7', '7'),
	('8', '8'),
	('9', '9'),
	('10', '10')])
	
	type = SelectField('Type', 
	choices=[('Basic', 'basic'),
	('Hero', 'hero'), 
	('Frog', 'frog'), 
	('Rainy Day', 'rainy_day'),
	('Social', 'social')])
	
	location = StringField('Location')
	
	link = StringField('Link')
	
	details = TextAreaField('Details')
	
	
	submit = SubmitField('create')
	
	
	
	
	
@app.route("/advanced_task_form", methods=['GET', 'POST'])
def advanced_task_form():

	form = Advanced_Task_Creation_Form()#if "GET", create form to send to template
	if form.validate_on_submit():

		title = form.title.data 
		start_date = form.start_date.data
		end_date = form.end_date.data
		reminder_date = form.reminder_date.data
		duration = form.duration.data
		recurrance = form.recurrance.data
		
		importance_rating = form.importance_rating.data
		energy_rating = form.energy_rating.data
		
		type = form.type.data
		location = form.location.data
		validators = form.validators.data
		link = form.link.date
		details = form.details.data

		if error:
			return render_template('list/dashboard_advanced_task_wtf.html', form=form)

	return render_template('list/dashboard_advanced_task_wtf.html', form=form)
	
	
	
	
	
	
	
	
	
	
	


