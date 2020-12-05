
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


class Module_Test(unittest.TestCase):
	
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
	def test_module(self):
		'''Test Comment for test_empty_db'''
		
		#Arrange
		
		#Act
		db_query = User.query.get(0)
		print("test_module")
		
		#Assert
		self.assertIsNone(db_query)


if __name__ == '__main__':
	unittest.main()
    #unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='example_dir'))