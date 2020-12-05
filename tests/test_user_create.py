
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


import HtmlTestRunner
from unittest_prettify.colorize import (
    colorize,
    GREEN,
    RED,
)


class User_Creation_Test(unittest.TestCase):
	
	def setUp(self):
		flask_app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/testing22.db'
		flask_app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
		flask_app.app.config['TESTING'] = True
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		
	#http://wiki.c2.com/?ArrangeActAssert
	
	@colorize(color=GREEN)
	def test_empty_db(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		
		#Act
		db_query = User.query.get(0)
		
		#Assert
		self.assertIsNone(db_query)

	#Test User creation from empty database
	def test_user_db(self):
	
		#Arrange
		db_query_before = db.session.query(User).filter(User.name == \
		"Yusef").first()

		#Act
		user_create_confirmed = user_create(\
		"Yusef", "fakeemail@my.yorku.ca", "asdfasdf")
		
		db_query_after = db.session.query(User).filter(User.name == \
		"Yusef").first()
		
		#Assert
		self.assertIsNone(db_query_before)
		self.assertTrue(user_create_confirmed)
		self.assertIsNotNone(db_query_after)
		self.assertIsNotNone(db_query_after.time_created)
		self.assertEqual(db_query_after.name, "Yusef")
		self.assertEqual(db_query_after.email, "fakeemail@my.yorku.ca")
		self.assertEqual(db_query_after.password, "asdfasdf")

	#Test List Create on User Creation
	def test_default_lists(self):
	
		#Arrange
		db_query_before = db.session.query(List).filter(List.title == \
		"Getting Started", List.parent_user == 1).first()
		
		user_create_confirm = user_create("Yusef", \
		"fakeemail@my.yorku.ca", "asdfasdf")
		
		#Act
		db_query_after = db.session.query(List).filter(List.title == \
		"Getting Started", List.parent_user == 1).first()
		
		#Assert
		self.assertIsNone(db_query_before)
		self.assertIsNotNone(db_query_after)
	
	#Test Task Create on User Creation
	def test_default_tasks(self):
	
		#Arrange
		db_query_before = db.session.query(Task).filter(Task.title == \
		"1984 By George Orwell", Task.parent_list == 2).first()
		
		user_create_confirm = user_create("Yusef", \
		"fakeemail@my.yorku.ca", "asdfasdf")
		
		#Act
		db_query_after = db.session.query(Task).filter(Task.title == \
		"1984 By George Orwell", Task.parent_list == 2).first()
		
		#Assert
		self.assertIsNone(db_query_before)
		self.assertIsNotNone(db_query_after)

if __name__ == '__main__':
	unittest.main()
    #unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='example_dir'))