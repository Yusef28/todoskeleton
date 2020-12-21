
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
from routes import *

import HtmlTestRunner
from unittest_prettify.colorize import (
    colorize,
    GREEN,
    RED,
)

class Dashboard_Test(unittest.TestCase):
	
	def setUp(self):
		flask_app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/testing28.db'
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
		
		
	def test_dashboard_index(self):
	
		#Arrange
		self.reg_log()
	
		#Act
		result = self.app.get("/index", follow_redirects=True)

		#Assert
		self.assertFalse(b'Getting Started' in result.data)
		
		
	def test_dashboard(self):
	
		#Arrange
		self.reg_log()
	
		#Act
		result = self.app.get("/dashboard", follow_redirects=True)

		#Assert
		self.assertTrue(b'Getting Started' in result.data)

	def test_dashboard_filter_all_current(self):
	
		#Arrange
		self.reg_log()
	
		#Act
		result = self.app.get("/dashboard", follow_redirects=True)
		
		#Assert
		self.assertTrue(b"Getting Started (6)</span> \n\t<span> Filter: All" in result.data)

	def test_dashboard_filter_all_completed(self):
	
		#Arrange
		self.reg_log()
	
		#Act
		result = self.app.get("/dashboard", follow_redirects=True)
		
		#Assert
		self.assertTrue(b"Getting Started (6)</span> \n\t<span> Filter: All" in result.data)

	def test_dashboard_filter_all_deleted(self):
	
		#Arrange
		self.reg_log()
	
		#Act
		result = self.app.get("/dashboard", follow_redirects=True)
		
		#Assert
		self.assertTrue(b"Getting Started (6)</span> \n\t<span> Filter: All" in result.data)

		
	def test_dashboard_important_before(self):
	
		#Arrange
		self.reg_log()
	
		#Act
		result = self.app.get("/filter_important", follow_redirects=True)

		#Assert
		self.assertTrue(b'Getting Started' in result.data)
		self.assertFalse(b'Try marking this task as completed!' in result.data)
		
		
	def test_dashboard_important_after(self):
	
		#Arrange
		self.reg_log()
	
		#Act
		self.app.get("task_important/1", follow_redirects=True)
		result = self.app.get("/filter_important", follow_redirects=True)

		#Assert
		self.assertTrue(b'Getting Started' in result.data)
		self.assertTrue(b'Try marking this task as completed!' in result.data)
		
		
	def test_dashboard_completed_before(self):
	
		#Arrange
		self.reg_log()
	
		#Act
		result = self.app.get("/filter_completed", follow_redirects=True)

		#Assert
		self.assertTrue(b'Getting Started' in result.data)
		self.assertFalse(b'Try marking this task as completed!' in result.data)
		
		
	def test_dashboard_completed_after(self):
	
		#Arrange
		self.reg_log()
	
		#Act
		self.app.get("task_completed/1", follow_redirects=True)
		result = self.app.get("/filter_completed", follow_redirects=True)
		
		#Assert
		self.assertTrue(b'Getting Started' in result.data)
		self.assertTrue(b'Try marking this task as completed!' in result.data)
		
	def test_dashboard_current_before(self):
	
		#Arrange
		self.reg_log()
	
		#Act
		result = self.app.get("/filter_current", follow_redirects=True)

		#Assert
		self.assertTrue(b'Getting Started' in result.data)
		self.assertTrue(b'Try marking this task as completed!' in result.data)
		
		
	def test_dashboard_current_after(self):
	
		#Arrange
		self.reg_log()
	
		#Act
		self.app.get("task_completed/1", follow_redirects=True)
		result = self.app.get("/filter_current", follow_redirects=True)
		
		#Assert
		self.assertTrue(b'Getting Started' in result.data)
		self.assertFalse(b'Try marking this task as completed!' in result.data)
		
	def test_dashboard_deleted_before(self):
	
		#Arrange
		self.reg_log()
	
		#Act
		result = self.app.get("/filter_deleted", follow_redirects=True)

		#Assert
		self.assertTrue(b'Getting Started' in result.data)
		self.assertFalse(b'Try marking this task as completed!' in result.data)
		
		
	def test_dashboard_deleted_after(self):
	
		#Arrange
		self.reg_log()
	
		#Act
		self.app.get("task_delete/1", follow_redirects=True)
		result = self.app.get("/filter_deleted", follow_redirects=True)
		
		#Assert
		self.assertTrue(b'Getting Started' in result.data)
		self.assertTrue(b'Try marking this task as completed!' in result.data)
		
	