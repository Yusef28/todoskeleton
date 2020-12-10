
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
		

	def test_task_create_post(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		self.reg_log()
		
		task_title = 'new task'
		
		data = dict(
		new_task=task_title
		)
		
		#Act
		result_before = db.session.query(Task).filter_by(
		parent_list = 1, 
		title=task_title).first()

		result = self.app.post(
		'/task_create', data=data, follow_redirects=True)
		
		result_after = db.session.query(Task).filter_by(\
		parent_list = 1, 
		title=task_title).first()

		#Assert
		self.assertIsNone(result_before)
		self.assertIsNotNone(result_after)
		

	def test_task_important(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		self.reg_log()
	
		#Act
		result_before = db.session.query(Task).filter_by(
		parent_list = 1, id = 1).first().important
		
		#change
		self.app.get("task_important/1", follow_redirects=True)
		#task_important(1)
		#is it in now?
		result_after = db.session.query(Task).filter_by(
		parent_list = 1, id = 1).first().important
		
		#Assert
		self.assertTrue(result_before == 0)
		self.assertTrue(result_after == 1)	
	
	def test_task_important_off(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		self.reg_log()
	
		#Act
		result_before = db.session.query(Task).filter_by(
		parent_list = 1, id = 1).first().important
		
		#change
		self.app.get("task_important/1", follow_redirects=True)
		self.app.get("task_important/1", follow_redirects=True)
		
		result_after = db.session.query(Task).filter_by(
		parent_list = 1, id = 1).first().important
		
		#Assert
		self.assertTrue(result_before == 0)
		self.assertTrue(result_after == 0)
	
	def test_task_completed(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		self.reg_log()
	
		#Act
		result_before = db.session.query(Task).filter_by(
		parent_list = 1, id = 1).first().completed 
		#change
		self.app.get("task_completed/1", follow_redirects=True)
		#task_completed(1)
		#is it in now?
		result_after = db.session.query(Task).filter_by(
		parent_list = 1, id = 1).first().completed 
		
		#Assert
		#self.assertTrue(result_before.completed == 0) errors with:
		#Error: "Instance <Task at 0x48b7630> is not bound to a Session; attribute refresh operation cannot proceed"
		self.assertTrue(result_before == 0)
		self.assertTrue(result_after == 1)

	def test_task_delete(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		self.reg_log()
	
		#Act
		result_before = db.session.query(Task).filter_by(
		parent_list = 1, id = 1).first().deleted

		#change
		result = self.app.get("task_delete/1", follow_redirects=True)
		#is it in now?
		result_after = db.session.query(Task).filter_by(
		parent_list = 1, id = 1).first().deleted
		
		#Assert
		
		#self.assertEqual(result_before.deleted, False) fails with "Failure: True != False"
		self.assertEqual(result_before, False)
		#self.assertEqual(result_before.current, 1)
		self.assertEqual(result_after, True)
		#self.assertEqual(result_after.current, 0)
		
	def test_task_delete_undo(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		self.reg_log()
	
		#Act
		result_before = db.session.query(Task).filter_by(
		parent_list = 1, id = 1).first()
		#double delete
		self.app.get("task_delete/1", follow_redirects=True)
		self.app.get("task_delete/1", follow_redirects=True)
		#is it in now?
		result_after = db.session.query(Task).filter_by(
		parent_list = 1, id = 1).first()
		
		#Assert
		self.assertIsNotNone(result_before)
		self.assertIsNone(result_after)
		print('ttdu gut')
		
	def test_task_delete_full(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		self.reg_log()
	
		#Act
		result_before = db.session.query(Task).filter_by(
		parent_list = 1, id = 1).first()
		#double delete
		self.app.get("task_delete/1", follow_redirects=True)
		self.app.get("task_delete_undo/1", follow_redirects=True)
		#is it in now?
		result_after = db.session.query(Task).filter_by(
		parent_list = 1, id = 1).first()
		
		#Assert
		self.assertIsNotNone(result_before)
		self.assertIsNotNone(result_after)
		print('ttdf gut')