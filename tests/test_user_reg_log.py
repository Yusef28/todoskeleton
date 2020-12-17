import datetime

from flask import Flask, redirect, render_template, request, url_for, session  #need session
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
		
	def test_login_wtf_get(self):
		
		#Assess

		#Act
		result = self.app.get('/login_wtf', follow_redirects=True)

		#Assert
		self.assertTrue(b"<h1>Login</h1>" in result.data)
		pass	
	
	def test_login_wtf_user_not_in(self):
		
		#Assess
		data = dict(
		username="Yusef",
		password="asdfasdf"
		)
		
		#Act
		result = self.app.post('/login_wtf', data=data , follow_redirects=True)

		#Assert
		self.assertTrue(b"User not found." in result.data)
		pass
		
	def test_login_wtf_user_not_in(self):
		
		#Assess
		self.register(
		"Yusef", 
		"fake_email@hotmail.com", 
		"asdfasdf", 
		"asdfasdf"
		)
		
		data = dict(
		username="Yusef",
		password="asdfghjk"
		)
		
		#Act
		result = self.app.post('/login_wtf', data=data , follow_redirects=True)

		#Assert
		self.assertTrue(b"User name or password False." in result.data)
		pass
		
	def test_login_wtf_result(self):
		
		#Assess
		self.register(
		"Yusef", 
		"fake_email@hotmail.com", 
		"asdfasdf", 
		"asdfasdf"
		)
		
		data = dict(
		username="Yusef",
		password="asdfasdf"
		)
		
		#Act
		result = self.app.post('/login_wtf', data=data , follow_redirects=True)

		#Assert
		self.assertTrue(b"Getting Started" in result.data)
		pass	
		
		
		
	def test_registration_wtf_get(self):
		
		#Assess

		#Act
		result = self.app.get('/registration_wtf', follow_redirects=True)

		#Assert
		self.assertTrue(b"<h1>Registration</h1>" in result.data)
		pass
	
	def test_registration_wtf_name_in(self):
		
		#Asses
		
		self.register("Yusef","email@hotmail.com","asdfasdf","asdfasdf")
		
		data = dict(
		username="Yusef",
		email="fake_email@hotmail.com",
		password="asdfasdf",
		password2="asdfasdf"
		)
		
		#Act
		result = self.app.post('/registration_wtf', data=data, follow_redirects=True)

		#Assert
		self.assertTrue(b"user name already registered." in result.data)
		pass
		
	def test_registration_wtf_email_in(self):
		
		self.register("Yusef2","fake_email@hotmail.com","asdfasdf","asdfasdf")
		
		data = dict(
		username="Yusef",
		email="fake_email@hotmail.com",
		password="asdfasdf",
		password2="asdfasdf"
		)
		
		#Act
		result = self.app.post('/registration_wtf', data=data, follow_redirects=True)

		
		#Assert
		self.assertTrue(b"user email already registered." in result.data)

		pass
		
	def test_registration_wtf_password_short(self):
		
		#Assess
		
		data = dict(
		username="Yusef",
		email="fake_email@hotmail.com",
		password="asdf",
		password2="asdf"
		)
		
		#Act
		result = self.app.post('/registration_wtf', data=data, follow_redirects=True)

		
		#Assert
		self.assertTrue(b"password must be at least 8 characters long." in result.data)

		pass
		
	def test_registration_wtf_password_mismatch(self):
		
		#Assess
		data = dict(
		username="Yusef",
		email="fake_email@hotmail.com",
		password="asdfasdf",
		password2="asdffghj"
		)
		
		#Act
		result = self.app.post('/registration_wtf', data=data, follow_redirects=True)

		#Assert
		self.assertTrue(b"password and confirmation password must match." in result.data)

		pass
		
	def test_registration_wtf_error(self):
		
		#Assess
		data = dict(
		username="Yusef",
		email="fake_email@hotmail.com",
		password="asdf",
		password2="asdf"
		)
		
		#Act
		result = self.app.post('/registration_wtf', data=data, follow_redirects=True)

		
		#Assert
		self.assertTrue(b"<h1>Registration</h1>" in result.data)

		pass
		
	def test_registration_wtf_result(self):
		
		#Assess
		data = dict(
		username="Yusef",
		email="fake_email@hotmail.com",
		password="asdfasdf",
		password2="asdfasdf"
		)
		
		#Act
		result = self.app.post('/registration_wtf', data=data, follow_redirects=True)

		
		#Assert
		self.assertTrue(b"<h1>Login</h1>" in result.data)

		pass
		
	
	
if __name__ == '__main__':
	unittest.main()
    #unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='example_dir'))