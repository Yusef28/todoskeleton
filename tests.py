
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

class TestCase(unittest.TestCase):
	
	def setUp(self):
		flask_app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/testing22.db'
		flask_app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
		flask_app.app.config['TESTING'] = True
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		
	def test_empty_db(self):
		rv = User.query.get(0)
		assert rv == None

		
	def test_user_db(self):
		rv = db.session.query(User).filter(User.name == "Yusef").first()
		assert rv == None
		rv = user_create("Yusef", "yusef28@my.yorku.ca", "asdfasdf")
		rv = db.session.query(User).filter(User.name == "Yusef").first()
		assert rv != None
		assert rv.name == "Yusef"
		
if __name__ == '__main__':
    unittest.main()