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

#fur datum
from sqlalchemy.sql import func
from sqlalchemy import DateTime, Date
#Modules
from app import db

class User(db.Model):

	__tablename__ = "users"

	#ich habe gehort das autoincrement hat kosten https://sqlite.org/autoinc.html
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(20), nullable=False)
	time_created = db.Column(DateTime(timezone=True), server_default=func.now())
	time_updated = db.Column(DateTime(timezone=True), onupdate=func.now())
	lists = relationship("List", cascade="all, delete")

class List(db.Model):

	__tablename__ = "lists"

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), unique=True, nullable=False)
	eltern_user = Column(Integer, ForeignKey('users.id'), nullable=False)
	tasks = relationship("Task", cascade="all, delete")
	time_created = db.Column(DateTime(timezone=True), server_default=func.now())
	time_updated = db.Column(DateTime(timezone=True), onupdate=func.now())


class Task(db.Model):

	__tablename__ = "tasks"

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	eltern_list = Column(Integer, ForeignKey('lists.id'), nullable=False)
	time_created = db.Column(DateTime(timezone=True), server_default=func.now())
	time_updated = db.Column(DateTime(timezone=True), onupdate=func.now())
	aktuelle = db.Column(Boolean, unique=False, default=True)
	wichtig = db.Column(Boolean, unique=False, default=False)
	geloscht = db.Column(Boolean, unique=False, default=False)
	fertig = db.Column(Boolean, unique=False, default=False)
