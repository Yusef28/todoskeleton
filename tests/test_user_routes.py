import datetime

from flask import Flask, redirect, render_template, request, url_for, session  #need session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
	Table, Column, Integer, String, MetaData, ForeignKey, Boolean
	)
	
from werkzeug.security import check_password_hash, generate_password_hash


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
from user_routes import user_read, user_update, user_delete

import HtmlTestRunner
from unittest_prettify.colorize import (
    colorize,
    GREEN,
    RED,
)


class Module_Test(unittest.TestCase):
	
	def setUp(self):
		flask_app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/testing23.db'
		flask_app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
		flask_app.app.config['TESTING'] = True
		
		#this line is from the stackoverflow link below
		flask_app.app.config['WTF_CSRF_ENABLED'] = False
		
		self.app = flask_app.app.test_client()
		db.create_all()
		
	def tearDown(self):
		db.session.remove()
		db.drop_all()
		
	#http://wiki.c2.com/?ArrangeActAssert
	
	
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
	# # # # # funtions where I have to get/post # # # # # # # #
	#because the function in te project requires the session object
	#and that comes from the test_client which is self.app
	
	#https://stackoverflow.com/questions/21577481/flask-wtf-wtforms-with-unittest-fails-validation-but-works-without-unittest
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

	def logout(self):
		#test client sends a get request to /logout
		return self.app.get('/logout', follow_redirects=True)
		
	def delete(self):
		#test client sends a get request to /logout
		return self.app.get('/user_delete', follow_redirects=True)
		
	# # # # # # end of get/post functions # # # # # # # # # # # 
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
	
	
	
	def test_user_register(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		user_before = User.query.filter_by(name = "Yusef").first()
		
		#Act
		result = self.register("Yusef", "fakeemail@my.yorku.ca", "asdfasdf", "asdfasdf")
		user_after = User.query.filter_by(name = "Yusef").first()
		
		#Assert
		self.assertIsNone(user_before)
		self.assertIsNotNone(user_after)
		self.assertTrue(user_after.name == "Yusef")
		self.assertTrue(b"Login" in result.data)
		
		
	def test_user_login(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		result_before = self.login("Yusef","asdfasdf")
		
		#Act
		self.register("Yusef", "fakeemail@my.yorku.ca", "asdfasdf", "asdfasdf")
		result_after = self.login("Yusef","asdfasdf")
		
		#Assert
		self.assertTrue(b"User not found." in result_before.data)
		self.assertTrue(b"User not found." not in result_after.data)
		#the only thing I'm not testing is that the session get's set.
		#at least I have this last assert here...
		self.assertTrue(b"Getting Started" in result_after.data)

		
	def test_user_logout(self):
		'''Test Comment for test_empty_db'''
		#Arrange
		self.register("Yusef", "fakeemail@my.yorku.ca", "asdfasdf", "asdfasdf")
		result_before = self.login("Yusef","asdfasdf")
		
		#Act
		result_after = self.logout()

		#Assert
		self.assertTrue(b"Getting Started" in result_before.data)
		self.assertTrue(b"Getting Started" not in result_after.data)
	
	def test_user_read(self):
		'''Test Comment for test_empty_db'''
		#Arrange
		user_create( \
		"Yusef", "fakeemail@my.yorku.ca", "asdfasdf")
		#Act
		result = user_read(1) == User.query.get(1)
		#Assert
		self.assertTrue(result)

	def test_user_update(self):
		'''Test Comment for test_empty_db'''
		#Arrange
		user_create( \
		"Yusef", "fakeemail@my.yorku.ca", "asdfasdf")
		name_before = User.query.get(1).name
		#Act
		user_update(1, "NewName")
		name_after = User.query.get(1).name

		#Assert
		self.assertEqual(name_before, "Yusef")
		self.assertEqual(name_after, "NewName")
		
	def test_user_delete(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		result_before = self.login("Yusef","asdfasdf")
		user_query_before = User.query.get(1)
		
		#Act
		self.register("Yusef", "fakeemail@my.yorku.ca", "asdfasdf", "asdfasdf")
		result_after = self.login("Yusef","asdfasdf")
		user_query_after = User.query.get(1)
		
		result_on_delete = self.delete()
		result_after_delete = self.login("Yusef","asdfasdf")
		user_query_after_delete = User.query.get(1)
		
		#Assert
		self.assertTrue(b"User not found." in result_before.data)
		self.assertTrue(b"User not found." not in result_after.data)
		self.assertTrue(b"User not found." in result_after_delete.data)
		
		self.assertIsNone(user_query_before)
		self.assertIsNotNone(user_query_after)
		self.assertIsNone(user_query_after_delete)

		#here again the only thing I don't test is that the session is destroyed
		
		


if __name__ == '__main__':
	unittest.main()
    #unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='example_dir'))