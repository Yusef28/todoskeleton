#!interpreter [optional-arg]
# -*- coding: utf-8 -*-
#
"""
models.py: All Models
"""

#Built-ins/Generic
import datetime

#Libs
from sqlalchemy import (
	Table, Column, Integer, String, MetaData, ForeignKey, Boolean
	)
from sqlalchemy.orm import relationship

#fur datum
from sqlalchemy.sql import func
from sqlalchemy import DateTime, Date
#Modules
from flask_app import db

class User(db.Model):

	__tablename__ = "users"

	#Autoincrement has costs https://sqlite.org/autoinc.html
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(200), nullable=False)
	time_created = db.Column(DateTime(timezone=True), server_default=func.now())
	
	lists = relationship("List", cascade="all, delete")
	
	#current_list = db.Column(db.Integer)
	
	time_zone = db.Column(db.String(80), unique=True, nullable=True, default=None)#must check if None
	list_count = db.Column(db.Integer, nullable=False, default=0)
	last_active = db.Column(DateTime(timezone=True), server_default=func.now())
	last_updated = db.Column(DateTime(timezone=True), nullable=True, default=None)#must check if None
	online = db.Column(Boolean, unique=False, default=False)
	
	#users_followers = db.Column(db.String(4056), unique=False, nullable=False, default="")
	#user_is_following = db.Column(db.String(4056), unique=False, nullable=False, default="")
	#saved_lists = db.Column(db.String(4056), unique=False, nullable=False, default="")
	
	bio = db.Column(db.String(4056), unique=False, nullable=False, default="")
	type = db.Column(db.String(80), unique=False, nullable=False, default="basic")#alpha, beta, basic, premium, anon
	css_theme = db.Column(db.String(4056), unique=False, nullable=False, default="styles.css")
	
	banned = db.Column(Boolean, unique=False, default=False)
	ban_severity = db.Column(db.Integer, nullable=False, default=0) #0,1,2 1=30 day, 2=life
	banned_until = db.Column(DateTime(timezone=True), nullable=True, default=None)#must check if None
	
	
class List(db.Model):

	__tablename__ = "lists"

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False)
	parent_user = Column(Integer, ForeignKey('users.id'), nullable=False)
	tasks = relationship("Task", cascade="all, delete")
	current = db.Column(Boolean, unique=False, default=False)
	time_created = db.Column(DateTime(timezone=True), server_default=func.now())
	
	# ################################### new task Columns #######################################
	
	#Count Columns
	all_count = db.Column(db.Integer, nullable=False, default=0)
	current_count = db.Column(db.Integer, nullable=False, default=0)
	important_count = db.Column(db.Integer, nullable=False, default=0)
	deleted_count = db.Column(db.Integer, nullable=False, default=0)
	completed_count = db.Column(db.Integer, nullable=False, default=0)
	last_updated = db.Column(DateTime(timezone=True), nullable=True, default=None)#must check if None
	
	#new 14-12-2020
	
	#sorting
	#sort_value = db.Column(db.Integer, nullable=False)#a value must be assigned at creation!!
	#sorted_by = db.Column(db.String(4056), unique=False, nullable=True, default=None)
	
	#type columns
	tags = db.Column(db.String(4056), unique=False, nullable=False, default="")
	categories = db.Column(db.String(4056), unique=False, nullable=False, default="")
	type = db.Column(db.String(80), unique=False, nullable=False, default="basic")
	
	#social columns
	likes = db.Column(db.Integer, nullable=False, default=0)
	privacy_type = db.Column(db.String(80), unique=False, nullable=False, default="private")#Private, #public, #group
	password = db.Column(db.String(200), unique=False, nullable=True, default=None)
	reported = db.Column(Boolean, unique=False, nullable=False, default=False)
	reported_by = db.Column(db.Integer, nullable=True, default=None)#User ID here
	
	#Analysis columns
	track = db.Column(Boolean, unique=False, nullable=False, default=False)
	
	#Time columns
	recycle_period_days = db.Column(db.Integer, nullable=False, default=0)
	
	
	#color columns
	color = db.Column(db.String(80), unique=False, nullable=True, default=None)#must check if none
	
	
class Task(db.Model):

	__tablename__ = "tasks"

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	parent_list = Column(Integer, ForeignKey('lists.id'), nullable=False)
	time_created = db.Column(DateTime(timezone=True), server_default=func.now())
	last_updated = db.Column(DateTime(timezone=True), nullable=True, default=None)#must check if None
	current = db.Column(Boolean, unique=False, default=True)
	important = db.Column(Boolean, unique=False, default=False)
	deleted = db.Column(Boolean, unique=False, default=False)
	completed = db.Column(Boolean, unique=False, default=False)
	#Neue
	state = db.Column(db.String(200), unique=False, nullable=True, default="current")#current, completed, current-deleted, completed-deleted
	
	# ################################### new task Columns #######################################
	#Neue
	sort_value = db.Column(db.Integer, nullable=False)#a value must be assigned at creation!!!
	
	#date/time columns
	start_date = db.Column(DateTime(timezone=True), nullable=True, default=None)#must check if none
	end_date = db.Column(DateTime(timezone=True), nullable=True, default=None)#must check if none
	reminder_date = db.Column(DateTime(timezone=True), nullable=True, default=None)
	duration_minutes = db.Column(db.Integer, nullable=True, default=None)#must check if none
	reoccurance_days = db.Column(db.Integer, nullable=True, default=None)#must check if none
	
	#color columns
	fg_color = db.Column(db.String(200), unique=False, nullable=True, default=None)#must check if none
	bg_color = db.Column(db.String(200), unique=False, nullable=True, default=None)#must check if none
	
	#rating/type columns
	type = db.Column(db.String(200), unique=False, nullable=True, default="basic")#Rainy, Frog, Hero, #basic
	importance_rating = db.Column(db.Integer, nullable=False, default=0)
	energy_rating = db.Column(db.Integer, nullable=False, default=1)
	
	#Advanced Tasks
	info = db.Column(db.String(8000), unique=False, nullable=True, default=None)#must check if none
	link = db.Column(db.String(2000), unique=False, nullable=True, default=None)#must check if none
	location = db.Column(db.String(2000), unique=False, nullable=True, default=None)#must check if none
	material = db.Column(db.String(8000), unique=False, nullable=True, default=None)#must check if none
	

class Admin_Blog(db.Model):

	__tablename__ = "admin_blog"
	
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=True, default='')
	body = db.Column(db.String(8000), nullable=True, default='')
	
	#smaller sizes so that it works in pythonanywheere without error 1118
	link = db.Column(db.String(200), unique=False, nullable=True, default=None)#must check if none
	foto_link = db.Column(db.String(200), unique=False, nullable=True, default=None)#must check if none
	signature = db.Column(db.String(200), unique=False, nullable=True, default="Yusef")
	
	time_created = db.Column(DateTime(timezone=True), server_default=func.now())
	pinned = db.Column(Boolean, unique=False, default=False)
	deleted = db.Column(Boolean, unique=False, default=False)
	
	#sort_order = Column(Integer, nullable=False)#a value must be assigned at creation!!!
	
	#type columns
	tags = db.Column(db.String(1000), unique=False, nullable=False, default="")
	categories = db.Column(db.String(1000), unique=False, nullable=False, default="")
	type = db.Column(db.String(80), unique=False, nullable=False, default="basic")
	
	last_updated = db.Column(DateTime(timezone=True), nullable=True, default=None)#must check if None
	
	