
import datetime


from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
	Table, Column, Integer, String, MetaData, ForeignKey, Boolean
	)


from flask_testing import TestCase
import unittest

import flask_app
from flask_app import db
import tempfile
import pytest
import os



import routes
from models import User, List, Task
from user_create import user_create
import user_routes
import task_routes
import task_time_routes
from task_routes import *
from list_routes import (list_create, list_update, list_delete, 
						find_current_list, 
						change_current_list)
						
from task_time_routes import *


import HtmlTestRunner
from unittest_prettify.colorize import (
    colorize,
    GREEN,
    RED,
)

class Task_Time_Test(unittest.TestCase):
	
	def setUp(self):
		flask_app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/testing27.db'
		flask_app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
		flask_app.app.config['TESTING'] = True
		
		#this line is from the stackoverflow link below
		flask_app.app.config['WTF_CSRF_ENABLED'] = False
		
		self.app = flask_app.app.test_client()
		db.create_all()
		
	def tearDown(self):
		db.session.remove()
		db.drop_all()
		
	def login(self, username, password):
	
		data = dict(
		username=username,
		password=password
		)
		#test client sends a post request to /login_wtf with dict data
		#if login_wtf accepts data when sent as post
		return self.app.post('/login_wtf', data=data , follow_redirects=True)

	def register(self, username, email, password, password2):
	
		data = dict(
		username=username,
		email=email,
		password=password,
		password2=password2
		)
		#test client sends a post request to /login_wtf with dict data
		#if login_wtf accepts data when sent as post
		return self.app.post('/registration_wtf', data=data, follow_redirects=True)

	def reg_log(self):

		self.register( \
		"Yusef", 
		"fakeemail@my.yorku.ca", 
		"asdfasdf", 
		"asdfasdf")
		
		self.login( \
		"Yusef", 
		"asdfasdf")
		
		return
	
	def create_new_list(self, list_title):
	
		data = dict(
		new_list = list_title
		)

		result = self.app.post(
		'/list_create', 
		data = data, 
		follow_redirects = True)
	
	def test_task_start_date_time_update(self):
	
		#Arrange
		self.reg_log()
		self.create_new_list("new_list")
		self.app.post('/task_create', data=dict(new_task='new_task_1'), 
		follow_redirects=True)
		
		#yyyy-MM-ddThh:mm
		data = dict(
		task_start_date="1999-06-25T02:40"
		)
		
		#Act
		task_before = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 1).first()
		task_start_date_before = task_before.start_date
		task_id = task_before.id
		print(str(task_id))
		self.app.post('/task_start_date_time_update/'+str(task_id), 
		data=data, 
		follow_redirects=True)
		
		task_after = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 1).first()
		task_start_date_after = task_after.start_date
		
		#Assert		
		self.assertEqual(task_start_date_before, None)
		self.assertEqual(datetime.datetime.strftime(task_start_date_after, 
		'%Y-%m-%dT%H:%M'), 
		"1999-06-25T02:40")
		pass
	
	def test_task_end_date_time_update(self):
	
		#Arrange
		self.reg_log()
		self.create_new_list("new_list")
		self.app.post('/task_create', data=dict(new_task='new_task_1'), 
		follow_redirects=True)
		
		#yyyy-MM-ddThh:mm
		data = dict(
		task_end_date="1999-06-25T02:40"
		)
		
		#Act
		task_before = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 1).first()
		task_end_date_before = task_before.end_date
		task_id = task_before.id

		self.app.post('/task_end_date_time_update/'+str(task_id), 
		data=data, 
		follow_redirects=True)
		
		task_after = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 1).first()
		task_end_date_after = task_after.end_date
		
		#Assert		
		self.assertEqual(task_end_date_before, None)
		self.assertEqual(datetime.datetime.strftime(task_end_date_after, 
		'%Y-%m-%dT%H:%M'), 
		"1999-06-25T02:40")
		pass
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

