# -*- coding: utf-8 -*-
"""
*Module* ``project.models``

This module defines the database tables used for the web application.

See Also:
	A quick example how to define a table with
	`Flask_SQLALchemy <https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/>`__

"""

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from . import db

class User(UserMixin, db.Model):
	"""
	Extend :login:`UserMixin <flask_login.UserMixin>` and
	:db:`db.Model <flask_sqlalchemy.SQLAlchemy>`.

	Store data of each user who uses the system to get the scores of their items calculated.

	Attributes:
		id (:sql-type:`db.Integer <Integer>`): automatically defined user-id
		username (:sql-type:`db.String <String>`): username
		email (:sql-type:`db.String <String>`): user's email
		password (:sql-type:`db.String <String>`): use method :security:`generate_password_hash() <generate_password_hash>` 
												to create user's hashed password
	"""
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15), index=True, unique=True, nullable=False)
	email = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(80), nullable=False)

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = generate_password_hash(password, method='sha256')

	def check_password(self, password):
		"""
		Use :security:`check_password_hash() <check_password_hash>` to
		check if given password from user and the password saved in table are the same.

		Args:
			password (str): given password from user

		Returns:
			bool: ``True`` if these two are the same, else ``False``.
		"""
		return check_password_hash(self.password, password)

	def get_id(self):
		"""
		Override :login:`UserMixin.get_id() <flask_login.UserMixin>` method to
		manage login in multi-login system.
		"""
		return f"user:{self.id}"


class Project(db.Model):
	"""
	Extend :db:`db.Model <flask_sqlalchemy.SQLAlchemy>`.

	Store data of each project uploaded by users.

	Attributes:
		id (:sql-type:`db.Integer <Integer>`): automatically defined project-id
		name (:sql-type:`db.String <String>`): project name
		description (:sql-type:`db.String <String>`): project description
		anno_number (:sql-type:`db.Integer <Integer>`): number of expected 
										annotations/annotators for this project
		best_def (:sql-type:`db.String <String>`): definition of '**best**'
		worst_def (:sql-type:`db.String <String>`): definition of '**worst**'
		n_items (:sql-type:`db.Integer <Integer>`): number of items in project
		p_name (:sql-type:`db.String <String>`): endpoint to this project
		mturk (:sql-type:`db.Boolean <Boolean>`): whether to upload this project 
										on `Mechanical Turk <https://www.mturk.com/>`__
		user_id (:sql-type:`db.Integer <Integer>`): id of user this project belongs to
		user (:sql-rel:`db.relationship <sqlalchemy.orm.relationship>`): ``many-to-one``
										relationship with :class:`User`
	"""
	__tablename__ = 'projects'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, nullable=False)
	description = db.Column(db.Text, nullable=False)
	anno_number = db.Column(db.Integer, nullable=False)
	best_def = db.Column(db.Text, nullable=False)
	worst_def = db.Column(db.Text, nullable=False)
	n_items = db.Column(db.Integer, nullable=False)
	p_name = db.Column(db.Text, unique=True, nullable=False)

	mturk = db.Column(db.Boolean)

	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	user = db.relationship('User', backref=db.backref('projects', order_by=id), lazy=True)

	def __init__(self, name, description, anno_number, best_def, \
				 worst_def, n_items, p_name, mturk=False, user=None):
		self.name = name
		self.description = description
		self.anno_number = anno_number
		self.best_def = best_def
		self.worst_def = worst_def
		self.n_items = n_items
		self.p_name = p_name
		self.mturk = mturk
		self.user = user


annotator_batch = db.Table('annotator_batch',
							db.Column('annotator_id', db.Integer, db.ForeignKey('annotators.id')),
							db.Column('batch_id', db.Integer, db.ForeignKey('batches.id')),
							db.PrimaryKeyConstraint('annotator_id', 'batch_id'))


class Batch(db.Model):
	"""
	Extend :db:`db.Model <flask_sqlalchemy.SQLAlchemy>`.

	Store data of each created batch from project.

	Attributes:
		id (:sql-type:`db.Integer <Integer>`): automatically defined batch-id
		size (:sql-type:`db.Integer <Integer>`): batch size
		keyword (:sql-type:`db.String <String>`): keyword for this batch 
										(only used in case of MTurk)
		hit_id (:sql-type:`db.String <String>`): endpoint to this batch 
										in annotator system with option MTurk
		project_id (:sql-type:`db.Integer <Integer>`): id of this batch's project
		project (:sql-rel:`db.relationship <sqlalchemy.orm.relationship>`): ``many-to-one`` 
										relationship with :class:`Project`
	"""
	__tablename__ = 'batches'

	id = db.Column(db.Integer, primary_key=True)
	size = db.Column(db.Integer, nullable=False)

	# for MTurk
	keyword = db.Column(db.String, unique=True)
	hit_id = db.Column(db.Text)

	project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
	project = db.relationship('Project', backref=db.backref('batches', order_by=id), lazy=True)

	def __init__(self, size, keyword=None, hit_id=None, project=None):
		self.size = size
		self.keyword = keyword
		self.hit_id = hit_id
		self.project = project


tuple_item = db.Table('tuple_item',
					db.Column('tuple_id', db.Integer, db.ForeignKey('tuples.id'), nullable=False),
					db.Column('item_id', db.Integer, db.ForeignKey('items.id'), nullable=False),
					db.PrimaryKeyConstraint('tuple_id', 'item_id'))


class Tuple(db.Model):
	"""
	Extend :db:`db.Model <flask_sqlalchemy.SQLAlchemy>`.

	Store data of each created tuple from project.

	Attributes:
		id (:sql-type:`db.Integer <Integer>`): automatically defined tuple-id
		batch_id (:sql-type:`db.Integer <Integer>`): id of this tuple's batch
		batch (:sql-rel:`db.relationship <sqlalchemy.orm.relationship>`): ``many-to-one`` 
															relationship with :class:`Batch`
		items (:sql-rel:`db.relationship <sqlalchemy.orm.relationship>`): ``many-to-many`` 
															relationship with :class:`Item`
	"""
	__tablename__ = 'tuples'

	id = db.Column(db.Integer, primary_key=True)

	batch_id = db.Column(db.Integer, db.ForeignKey('batches.id'), nullable=False)
	batch = db.relationship('Batch', backref=db.backref('tuples', order_by=id), lazy=True)

	items = db.relationship('Item', secondary=tuple_item, backref=db.backref('tuples', lazy=True))

	def __init__(self, batch=None):
		self.batch = batch


class Item(db.Model):
	"""
	Extend :db:`db.Model <flask_sqlalchemy.SQLAlchemy>`.

	Store data of each uploaded item from project.

	Attributes:
		id (:sql-type:`db.Integer <Integer>`): automatically defined item-id
		item (:sql-type:`db.String <String>`): (raw) representation of item in string-format
	"""
	__tablename__ = 'items'

	id = db.Column(db.Integer, primary_key=True)
	item = db.Column(db.Text, unique=True, nullable=False)

	def __init__(self, item):
		self.item = item


class Annotator(UserMixin, db.Model):
	"""
	Extend :login:`UserMixin <flask_login.UserMixin>` and
	:db:`db.Model <flask_sqlalchemy.SQLAlchemy>`.

	Store data of each (local) annotator from project.

	Attributes:
		id (:sql-type:`db.Integer <Integer>`): automatically defined annotator-id
		keyword (:sql-type:`db.String <String>`): logged in keyword for annotator
		name (:sql-type:`db.String <String>`): pseudoname chosen by annotator to 
			avoid more annotators having access to annotator system using the same keyword
		project_id (:sql-type:`db.Integer <Integer>`): id of the project 
														the annotator takes part in
		project (:sql-rel:`db.relationship <sqlalchemy.orm.relationship>`): ``many-to-one`` 
														relationship with :class:`Project`
		batches (:sql-rel:`db.relationship <sqlalchemy.orm.relationship>`): ``many-to-many`` 
														relationship with :class:`Batch`
	"""
	__tablename__ = 'annotators'

	id = db.Column(db.Integer, primary_key=True)
	keyword = db.Column(db.String(50), unique=True)
	name = db.Column(db.String(50))

	project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
	project = db.relationship('Project', backref=db.backref('annotators', order_by=id), lazy=True)

	batches = db.relationship('Batch', secondary=annotator_batch, backref=db.backref('annotators', lazy=True))

	def __init__(self, keyword=None, name=None, project=None):
		self.keyword = keyword
		self.name = name
		self.project = project

	def get_id(self):
		"""
		Override :login:`UserMixin.get_id() <flask_login.UserMixin>` method
		to manage login in multi-login system.
		"""
		return f"annotator:{self.id}"


class Data(db.Model):
	"""
	Extend :db:`db.Model <flask_sqlalchemy.SQLAlchemy>`.

	Store data of each created tuple from project.

	Attributes:
		id (:sql-type:`db.Integer <Integer>`): automatically defined data-id
		best_id (:sql-type:`db.Integer <Integer>`): id of item chosen as '**best**'
												in table :class:`Item`
		worst_id (:sql-type:`db.Integer <Integer>`): id of item chosen as '**worst**'
												in table :class:`Item`
		anno_id (:sql-type:`db.Integer <Integer>`): id of annotator who submits/saves 
												this data (only in local annotator system)
		tuple_id (:sql-type:`db.Integer <Integer>`): id of the tuple this data uses
		annotator (:sql-rel:`db.relationship <sqlalchemy.orm.relationship>`): ``many-to-one`` 
												relationship with :class:`Annotator`
		tuple_ (:sql-rel:`db.relationship <sqlalchemy.orm.relationship>`): ``many-to-one``
												relationship with :class:`Tuple`
	"""
	__tablename__ = 'datas'

	id = db.Column(db.Integer, primary_key=True)

	best_id = db.Column(db.Integer, db.ForeignKey('items.id'))
	worst_id = db.Column(db.Integer, db.ForeignKey('items.id'))

	anno_id = db.Column(db.Integer, db.ForeignKey('annotators.id'), nullable=True)
	annotator = db.relationship('Annotator', backref=db.backref('datas', order_by=id), lazy=True)

	tuple_id = db.Column(db.Integer, db.ForeignKey('tuples.id'), nullable=False)
	tuple_ = db.relationship('Tuple', backref=db.backref('datas', order_by=id), lazy=True)

	def __init__(self, best_id=None, worst_id=None, annotator=None, tuple_=None):
		self.best_id = best_id
		self.worst_id = worst_id
		self.annotator = annotator
		self.tuple_ = tuple_
		