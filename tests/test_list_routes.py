
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
		flask_app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/testing25.db'
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
		
	#maybe there isn't ever a get call? So no referrer for that call?
	def test_list_create_get(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		self.reg_log()
		
		list_title = 'new list'
		
		#Act
		result = self.app.get(
		'/list_create', follow_redirects=True)
		
		#Assert
		#print(result.data)
		#self.assertTrue(b'Getting Started' in result.data)
	
	def test_list_create_post(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		self.reg_log()
		
		list_title = 'new list'
		
		data = dict(
		new_list=list_title
		)
		
		#Act
		result_before = db.session.query(List).filter_by(
		parent_user = 1, 
		title=list_title).first()

		result = self.app.post(
		'/list_create', data=data, follow_redirects=True)
		
		result_after = db.session.query(List).filter_by(\
		parent_user = 1, 
		title=list_title).first()

		#Assert
		self.assertIsNone(result_before)
		self.assertIsNotNone(result_after)
		
	def test_list_create_invalid(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		self.reg_log()
		
		list_title = 'Getting Started'
		
		data = dict(
		new_list=list_title
		)
		
		#Act
		result_before = db.session.query(List).filter_by(
		parent_user = 1, 
		id=5).first()

		result = self.app.post(
		'/list_create', data=data, follow_redirects=True)
		
		result_after = db.session.query(List).filter_by(\
		parent_user = 1, 
		id=5).first()

		#Assert
		self.assertIsNone(result_before)
		self.assertIsNone(result_after)
	
	def test_list_update_get(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		self.reg_log()
		#Act
		result = self.app.get("list_update", follow_redirects=True)
		#Assert
		#print(result.data)
		self.assertTrue(b'404 Not Found' in result.data)
		
		
	def test_list_update_post(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		self.reg_log()
		new_list_title = 'Good Book'
		data = dict(
		list_title_change_input = 'Good Book'
		)
		
		#Act
		result_before = db.session.query(List).filter_by(
		parent_user = 1, title=new_list_title).first()
		
		result = self.app.post("list_update/2", data=data, follow_redirects=True)
		
		result_after = db.session.query(List).filter_by(
		parent_user = 1, title=new_list_title).first()
		
		#Assert
		self.assertTrue(b'Getting Started' in result.data)
		self.assertIsNone(result_before)
		self.assertIsNotNone(result_after)
		
	def test_list_update_post_invalid(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		self.reg_log()
		
		new_list_title = 'Getting Started'
		
		data = dict(
		list_title_change_input = new_list_title
		)
		
		#Act
		#is it in?
		result_before = db.session.query(List).filter_by(
		parent_user = 1, title=new_list_title).first()
		#change
		result = self.app.post("list_update/2", data=data, follow_redirects=True)
		#is it in now?
		result_after = db.session.query(List).filter_by(
		parent_user = 1, title=new_list_title).first()
		
		#Assert
		#print(result.data)
		self.assertTrue(b'A list with this name already exists' in result.data)
		self.assertIsNotNone(result_before)
		self.assertIsNotNone(result_after)	
		
	#this actually tests deletion of a list that is NOT current, so this is a future feature
	def test_list_delete(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		self.reg_log()

		#Act
		result_before = db.session.query(List).filter_by(
		parent_user = 1, id = 2).first()
		
		#here it is get but we need self.app because we use session in list_delete()
		result = self.app.get("list_delete/2", follow_redirects=True)
		
		result_after = db.session.query(List).filter_by(
		parent_user = 1, id = 2).first()
		
		#Assert
		self.assertTrue(b'Getting Started' in result.data)
		self.assertIsNotNone(result_before)
		self.assertIsNone(result_after)
		
	def test_list_delete_invalid(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		self.reg_log()

		#Act
		result_before = db.session.query(List).filter_by(
		parent_user = 1, id = 1).first()
		
		#here it is get but we need self.app because we use session in list_delete()
		result = self.app.get("list_delete/1", follow_redirects=True)
		
		result_after = db.session.query(List).filter_by(
		parent_user = 1, id = 1).first()
		
		#Assert
		self.assertTrue(b'You cannot delete the Getting Started list!' in result.data)
		self.assertIsNotNone(result_before)
		self.assertIsNotNone(result_after)
		
	def test_list_delete_current(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		self.reg_log()
		result_title_before_change = db.session.query(List).filter_by(
		parent_user = 1, current=1).first().title		
		
		result = self.app.get("/change_current_list/1/2", follow_redirects=True)
		
		result_title_after_change = db.session.query(List).filter_by(
		parent_user = 1, current=1).first().title

		#Act

		#here it is get but we need self.app because we use session in list_delete()
		result = self.app.get("list_delete/2", follow_redirects=True)
		
		result_after_delete = db.session.query(List).filter_by(
		parent_user = 1, id = 2).first()
		
		#Assert
		self.assertEqual('Getting Started', result_title_before_change)
		self.assertEqual('Good Books', result_title_after_change)
		self.assertIsNone(result_after_delete)
		
	def test_find_current_list(self):
		
		#assess
		self.reg_log()
		current_list_query = db.session.query(List).filter_by(parent_user=1, current=1).first()
		lists = db.session.query(List).filter_by(parent_user=1).all()
		
		#act
		current_list_from_function = find_current_list(lists)
		
		#assert
		self.assertEqual(current_list_query.id, current_list_from_function.id)
		self.assertEqual(current_list_query.title, current_list_from_function.title)
		
		
	def test_change_current_list_good(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		self.reg_log()
		initial_current_list = 1
		new_current_list = 2
		current_list_before = db.session.query(List).filter_by(parent_user=1, current=1).first()
		
		#Act
		result = self.app.get("/change_current_list/"+str(initial_current_list)+"/"+str(new_current_list), follow_redirects=True)
		current_list_after = db.session.query(List).filter_by(parent_user=1, current=1).first()
		
		#Assert
		self.assertNotEqual(current_list_before.id, current_list_after.id)
		self.assertEqual(current_list_before.id, 1)
		self.assertEqual(current_list_after.id, 2)
		self.assertEqual(current_list_after.title, "Good Books")
		#self.assertTrue("Good Books" in result.data)
		#self.assertTrue("Getting Started" not in result.data)
		
		
	def test_change_invalid_list(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		self.reg_log()
		
		initial_current_list = 1
		new_current_list = 10
		current_list_before = db.session.query(List).filter_by(parent_user=1, current=1).first()
		
		#Act
		#result.data = change_current_list(initial_current_list, new_current_list)
		#here I still need a self.app.get() or else it says need to push an app context before using return redirect(url_for...
		result = self.app.get("/change_current_list/"+str(initial_current_list)+"/"+str(new_current_list), follow_redirects=True)
		current_list_after = db.session.query(List).filter_by(parent_user=1, current=1).first()
		
		#Assert
		self.assertEqual(current_list_before.id, current_list_after.id)
		self.assertEqual(current_list_before.id, 1)
		self.assertEqual(current_list_after.id, 1)
		self.assertEqual(current_list_after.title, "Getting Started")
		#self.assertTrue("Good Books" not in result.data)
		#self.assertTrue("Getting Started" in result.data)
		
	def test_change_same_list(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		self.reg_log()
		
		initial_current_list = 1
		new_current_list = 1
		current_list_before = db.session.query(List).filter_by(parent_user=1, current=1).first()
		
		#Act
		#result.data = change_current_list(initial_current_list, new_current_list)
		#here I still need a self.app.get() or else it says need to push an app context before using return redirect(url_for...
		result = self.app.get("/change_current_list/"+str(initial_current_list)+"/"+str(new_current_list), follow_redirects=True)
		current_list_after = db.session.query(List).filter_by(parent_user=1, current=1).first()
		
		#Assert
		self.assertEqual(current_list_before.id, current_list_after.id)
		self.assertEqual(current_list_before.id, 1)
		self.assertEqual(current_list_after.id, 1)
		self.assertEqual(current_list_after.title, "Getting Started")	

