#!interpreter [optional-arg]
# -*- coding: utf-8 -*-


"""
app.py: 
"""

#Built-in/Generic Imports
import datetime

#Libs
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
	Table, Column, Integer, String, MetaData, ForeignKey, Boolean
	)

#test stff
from flask_testing import TestCase
import unittest
#pallets test
import flask_app
import tempfile
import pytest
import os


#Modules
import routes
from models import User, List, Task
from user_create import user_create
import user_routes

@pytest.fixture
def client():
	
	#db_fd, flask_app.app.config['DATABASE'] = tempfile.mkstemp()[0], 'sqlite:////tmp/testing21.db'
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/testing22.db'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['TESTING'] = True
	
	db = SQLAlchemy(app)
	
	with app.test_client() as client:
		with app.app_context():
			db.create_all()
		yield client
		
	os.close(db)
	os.unlink(flask_app.app.config['SQLALCHEMY_DATABASE_URI'])
	db.session.remove()
	db.drop_all()
		
def test_empty_db():
	
	rv = User.query.get(0)
	assert rv == None

#user_create
	
def test_user_db():
	
	rv = user_create("Yuse2f", "yusef238@my.yorku.ca", "asdfasdf")
	assert rv == True
	
	
#if __name__ == "__main__":
#	unittest.main()

