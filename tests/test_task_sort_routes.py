
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
from task_routes import *
from list_routes import (list_create, list_update, list_delete, 
						find_current_list, 
						change_current_list)


import HtmlTestRunner
from unittest_prettify.colorize import (
    colorize,
    GREEN,
    RED,
)

class List_Test(unittest.TestCase):
	
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
		#when you create a new list it automatically
		#makes that list the new list.
		#That's the only way the following tests can work. 
		#They assume the new list is current.
		
	def test_task_create_sorted(self):
	
		#Arrange
		self.reg_log()
		self.create_new_list("new_list")
		
		data = dict(
		new_task='new_task'
		)
		
		task_exists_result_before = db.session.query(Task).filter_by(
		parent_list = 5, title = "new_task").first()
		
		#Act
		result = self.app.post(
		'/task_create', 
		data=data, 
		follow_redirects=True)
		
		task_exists_result_after = db.session.query(Task).filter_by(
		parent_list = 5, title = "new_task").first()
		
		#Assert		
		self.assertFalse(task_exists_result_before)
		self.assertTrue(task_exists_result_after)
		self.assertEqual(task_exists_result_after.sort_value, 1)
		pass

	def test_task_create_3_sorted(self):
	
		#Arrange
		self.reg_log()
		self.create_new_list("new_list")
		
		#Act
		self.app.post('/task_create', data=dict(new_task='new_task_1'), 
		follow_redirects=True)
		self.app.post('/task_create', data=dict(new_task='new_task_2'),
		follow_redirects=True)
		self.app.post('/task_create', data=dict(new_task='new_task_3'), 
		follow_redirects=True)
		
		task_1_exists_result_after = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 1).first()
		task_2_exists_result_after = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 2).first()
		task_3_exists_result_after = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 3).first()
		
		#Assert		
		self.assertEqual(task_1_exists_result_after.title, 'new_task_1')
		self.assertEqual(task_2_exists_result_after.title, 'new_task_2')
		self.assertEqual(task_3_exists_result_after.title, 'new_task_3')
		pass
	
	
	def test_task_delete_sorted_first(self):
	
		#Arrange
		self.reg_log()
		self.create_new_list("new_list")
		
		#Act
		self.app.post('/task_create', data=dict(new_task='new_task_1'), 
		follow_redirects=True)
		self.app.post('/task_create', data=dict(new_task='new_task_2'),
		follow_redirects=True)
		self.app.post('/task_create', data=dict(new_task='new_task_3'), 
		follow_redirects=True)
		
		task_in_first_position_before = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 1).first()
		
		task_in_first_position_before_id = task_in_first_position_before.id
		task_in_first_position_before_title = task_in_first_position_before.title
		self.app.get("task_delete/"+str(task_in_first_position_before_id), follow_redirects=True)
		#self.app.get("task_delete/"+str(id), follow_redirects=True)
		
		task_in_first_position_after = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 1).first()
		task_in_first_position_after_title = task_in_first_position_after.title
		
		#Assert		
		self.assertEqual(task_in_first_position_before_title,
		"new_task_1")
		self.assertEqual(task_in_first_position_after_title,
		"new_task_2")
		
		pass

	
	def test_task_delete_sorted_last(self):
	
		#Arrange
		self.reg_log()
		self.create_new_list("new_list")
		
		#Act
		self.app.post('/task_create', data=dict(new_task='new_task_1'), 
		follow_redirects=True)
		self.app.post('/task_create', data=dict(new_task='new_task_2'),
		follow_redirects=True)
		self.app.post('/task_create', data=dict(new_task='new_task_3'), 
		follow_redirects=True)
		
		task_in_last_position_before = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 3).first()
		
		id = task_in_last_position_before.id
		
		self.app.get("task_delete/"+str(id), follow_redirects=True)
		#self.app.get("task_delete/"+str(id), follow_redirects=True)
		
		task_in_last_position_after = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 3).first()
		
		#Assert
		self.assertTrue(task_in_last_position_before)
		self.assertFalse(task_in_last_position_after)
		
		pass	
	
	
	def test_task_delete_sorted_middle(self):
	
		#Arrange
		self.reg_log()
		self.create_new_list("new_list")
		
		#Act
		self.app.post('/task_create', data=dict(new_task='new_task_1'), 
		follow_redirects=True)
		self.app.post('/task_create', data=dict(new_task='new_task_2'),
		follow_redirects=True)
		self.app.post('/task_create', data=dict(new_task='new_task_3'), 
		follow_redirects=True)
		
		task_in_mid_position_before = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 2).first()
		
		task_in_mid_position_before_id = task_in_mid_position_before.id
		task_in_mid_position_before_title = task_in_mid_position_before.title
		
		self.app.get("task_delete/"+str(task_in_mid_position_before_id), follow_redirects=True)
		
		task_in_mid_position_after = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 2).first()
		task_in_mid_position_after_title = task_in_mid_position_after.title
		#Assert
		self.assertEqual(task_in_mid_position_before_title, 'new_task_2')
		self.assertEqual(task_in_mid_position_after_title, 'new_task_3')
		
		pass	
	
	def test_task_complete_sorted_middle(self):
	
		#Arrange
		self.reg_log()
		self.create_new_list("new_list")
		
		#Act
		self.app.post('/task_create', data=dict(new_task='new_task_1'), 
		follow_redirects=True)
		self.app.post('/task_create', data=dict(new_task='new_task_2'),
		follow_redirects=True)
		self.app.post('/task_create', data=dict(new_task='new_task_3'), 
		follow_redirects=True)
		
		task_in_mid_position_before = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 2).first()
		
		task_in_mid_position_before_id = task_in_mid_position_before.id
		task_in_mid_position_before_title = task_in_mid_position_before.title
		
		self.app.get("task_completed/"+str(task_in_mid_position_before_id), follow_redirects=True)
		
		task_in_mid_position_after = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 2).first()
		task_in_mid_position_after_title = task_in_mid_position_after.title
		#Assert
		self.assertEqual(task_in_mid_position_before_title, 'new_task_2')
		self.assertEqual(task_in_mid_position_after_title, 'new_task_3')
		
		pass	
	
	def test_task_sort_top(self):
		#Arrange
		self.reg_log()
		self.create_new_list("new_list")
		
		#Act
		self.app.post('/task_create', data=dict(new_task='new_task_1'), 
		follow_redirects=True)
		self.app.post('/task_create', data=dict(new_task='new_task_2'),
		follow_redirects=True)
		self.app.post('/task_create', data=dict(new_task='new_task_3'), 
		follow_redirects=True)
		
		task_before = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 1).first()
		
		id = task_before.id
		
		self.app.get("task_sort_up/"+str(id), follow_redirects=True)
		
		task_after = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 1).first()
		
		#Assert
		self.assertEqual(task_before.title, 'new_task_1')
		self.assertEqual(task_after.title, 'new_task_1')
		pass
		
	def test_task_sort_up(self):
		#Arrange
		self.reg_log()
		self.create_new_list("new_list")
		
		#Act
		self.app.post('/task_create', data=dict(new_task='new_task_1'), 
		follow_redirects=True)
		self.app.post('/task_create', data=dict(new_task='new_task_2'),
		follow_redirects=True)
		self.app.post('/task_create', data=dict(new_task='new_task_3'), 
		follow_redirects=True)
		
		task_before = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 2).first()
		task_before_title = task_before.title
		id = task_before.id
		
		self.app.get("task_sort_up/"+str(id), follow_redirects=True)
		
		task_after = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 2).first()
		task_after_title = task_after.title
		#Assert
		self.assertEqual(task_before_title, 'new_task_2')
		self.assertEqual(task_after_title, 'new_task_1')
		pass
		
	
		
	def test_task_sort_down(self):
		#Arrange
		self.reg_log()
		self.create_new_list("new_list")
		
		#Act
		self.app.post('/task_create', data=dict(new_task='new_task_1'), 
		follow_redirects=True)
		self.app.post('/task_create', data=dict(new_task='new_task_2'),
		follow_redirects=True)
		self.app.post('/task_create', data=dict(new_task='new_task_3'), 
		follow_redirects=True)
		
		task_before = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 2).first()
		task_before_title = task_before.title
		id = task_before.id
		
		self.app.get("task_sort_down/"+str(id), follow_redirects=True)
		
		task_after = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 2).first()
		task_after_title = task_after.title
		#Assert
		self.assertEqual(task_before_title, 'new_task_2')
		self.assertEqual(task_after_title, 'new_task_3')
		pass
		
	
	def test_task_sort_bottom(self):
		#Arrange
		self.reg_log()
		self.create_new_list("new_list")
		
		#Act
		self.app.post('/task_create', data=dict(new_task='new_task_1'), 
		follow_redirects=True)
		self.app.post('/task_create', data=dict(new_task='new_task_2'),
		follow_redirects=True)
		self.app.post('/task_create', data=dict(new_task='new_task_3'), 
		follow_redirects=True)
		
		task_before = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 3).first()
		task_before_title = task_before.title
		id = task_before.id
		
		self.app.get("task_sort_down/"+str(id), follow_redirects=True)
		
		task_after = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 3).first()
		task_after_title = task_after.title
		#Assert
		self.assertEqual(task_before_title, 'new_task_3')
		self.assertEqual(task_after_title, 'new_task_3')
		pass
		
		
	
	def test_task_sort_deleted_undo(self):	
		#Arrange
		self.reg_log()
		self.create_new_list("new_list")
		
		#Act
		self.app.post('/task_create', data=dict(new_task='new_task_1'), 
		follow_redirects=True)
		self.app.post('/task_create', data=dict(new_task='new_task_2'),
		follow_redirects=True)
		self.app.post('/task_create', data=dict(new_task='new_task_3'), 
		follow_redirects=True)
		
		task_in_mid_position_before = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 2).first()
		
		task_in_mid_position_before_id = task_in_mid_position_before.id
		task_in_mid_position_before_title = task_in_mid_position_before.title
		
		self.app.get("task_delete/"+str(task_in_mid_position_before_id), follow_redirects=True)
		self.app.get("task_delete_undo/"+str(task_in_mid_position_before_id), follow_redirects=True)
		
		task_in_mid_position_after = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 2).first()
		task_in_mid_position_after_title = task_in_mid_position_after.title
		
		task_in_last_position_after = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 3).first()
		task_in_last_position_after_title = task_in_last_position_after.title
		
		#Assert
		self.assertEqual(task_in_mid_position_before_title, 'new_task_2')
		self.assertEqual(task_in_mid_position_after_title, 'new_task_3')
		self.assertEqual(task_in_last_position_after_title, 'new_task_2')
		
	def test_task_sort_completed_undo(self):	
		#Arrange
		self.reg_log()
		self.create_new_list("new_list")
		
		#Act
		self.app.post('/task_create', data=dict(new_task='new_task_1'), 
		follow_redirects=True)
		self.app.post('/task_create', data=dict(new_task='new_task_2'),
		follow_redirects=True)
		self.app.post('/task_create', data=dict(new_task='new_task_3'), 
		follow_redirects=True)
		
		task_in_mid_position_before = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 2).first()
		
		task_in_mid_position_before_id = task_in_mid_position_before.id
		task_in_mid_position_before_title = task_in_mid_position_before.title
		
		self.app.get("task_completed/"+str(task_in_mid_position_before_id), follow_redirects=True)
		self.app.get("task_completed/"+str(task_in_mid_position_before_id), follow_redirects=True)
		
		task_in_mid_position_after = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 2).first()
		task_in_mid_position_after_title = task_in_mid_position_after.title
		
		task_in_last_position_after = db.session.query(Task).filter_by(
		parent_list = 5, sort_value = 3).first()
		task_in_last_position_after_title = task_in_last_position_after.title
		
		#Assert
		self.assertEqual(task_in_mid_position_before_title, 'new_task_2')
		self.assertEqual(task_in_mid_position_after_title, 'new_task_3')
		self.assertEqual(task_in_last_position_after_title, 'new_task_2')
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

