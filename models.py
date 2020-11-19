#!interpreter [optional-arg]
# -*- coding: utf-8 -*-

"""
models.py: Alle Models fur projekt
"""

#Built-ins/Generic
import datetime

#Libs
from sqlalchemy import (
	Table, Column, Integer, String, MetaData, ForeignKey, Boolean
	)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

#Modules
from app import db

class User(db.Model):

	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(4096), unique=True)
	email = db.Column(db.String(4096), unique=True)
	password = db.Column(db.String(4096))
	time_created = db.Column(DateTime(timezone=True), server_default=func.now())
	time_updated = db.Column(DateTime(timezone=True), onupdate=func.now())

	#remember = db.Column(Boolean, unique=False, default=False)

	lists = relationship("List", cascade="all, delete")
#	children = relationship(
#		"List", back_populates="parent",
#		cascade="all, delete",
#		passive_deletes=True
#   )

class List(db.Model):

	__tablename__ = "lists"

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(4096), unique=True)
	eltern_user = Column(Integer, ForeignKey('users.id'))
	tasks = relationship("Task", cascade="all, delete")
	time_created = db.Column(DateTime(timezone=True), server_default=func.now())
	time_updated = db.Column(DateTime(timezone=True), onupdate=func.now())

#	parent_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
#	parent = relationship("User", back_populates="children")

	#children = relationship(
#		"Task", back_populates="parent",
#		cascade="all, delete",
#		passive_deletes=True
#		)
		
		
class Task(db.Model):

	__tablename__ = "tasks"

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(4096))
	eltern_list = Column(Integer, ForeignKey('lists.id'))
	time_created = db.Column(DateTime(timezone=True), server_default=func.now())
	time_updated = db.Column(DateTime(timezone=True), onupdate=func.now())

	#parent_id = Column(Integer, ForeignKey('lists.id', ondelete="CASCADE"))
	#parent = relationship("List", back_populates="children")
	#id = db.Column(db.Integer, primary_key=True)
	#content = db.Column(db.String(4096))
	aktuelle = db.Column(Boolean, unique=False, default=True)
	wichtig = db.Column(Boolean, unique=False, default=False)
	geloscht = db.Column(Boolean, unique=False, default=False)
	fertig = db.Column(Boolean, unique=False, default=False)

	
