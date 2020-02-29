# -*- coding: utf-8 -*-
"""
Helper Functions
*****************

*Module* ``project.user.helpers`` 

This module provides some helper functions to deal with problems
of each subroute inside User-System.

"""

import string, random
from datetime import date
from werkzeug.utils import secure_filename
from ..generator import DataGenerator
from ..validators import allowed_file

def is_not_current_user(user, current_name):
	"""
	Inside the User-System, if a user is logged in and authenticated, 
	this user is not allowed to see profile of an another user by typing the route!
	If this meets the conditions which means the current user tries to access to 
	the account of an another user, this current user will be redirected to the login page
	and asked to log in with the used username.

	Args:
		user (:local:`werkzeug.LocalProxy <werkzeug.local.LocalProxy>`): this is actually 
								the attribute :login:`current_user <flask_login.current_user>`
		current_name (str): name of the other user to be typed in the route

	Returns: 
		bool: ``True`` if this is not the current user else ``False``
	"""
	return user and user.is_authenticated and current_name != user.username


def upload_file(files):
	"""
	Upload all files and store in container for later use.

	Args:
		files (list(:dat-struct:`FileStorage <werkzeug.datastructures.FileStorage>`)): list of uploaded files
	
	Returns:
		generator.DataGenerator: object that contains list of items, batches and tuples 
		if the number of items meeth the required condition

	Warning:
		* Returns 1 if there are items but the number is fewer than 5.
		* Returns None if there is no item at all.
	"""

	# create DataGenerator object
	data = DataGenerator()

	# keep updating datas for all validated uploaded files
	for file in files:
		if file and allowed_file(file.filename):
			data.generate_items(file)

	# check if the items after all meet the requirements of the project:
	# There must be at least 5 items for this project to be relevant
	if len(data.items) <= data.tuple_size:
		if len(data.items) == 0:
			return None
		else:
			return 1

	# generate data, this generates the batches and tuples from the given items
	data.generate_data()

	return data


def generate_keyword(chars=None, k_length=None):
	"""
	Generate keyword for annotators and batches.

	Args:
		chars (str): type of characters used to generate keyword, 
				*default:* ``string.ascii_letters+string.digits``
		k_length (int): length of the keyword, *default:* ``random.randint(8,12)``
	
	Returns: 
		str: generated keyword

	Examples:
		>>> generate_keyword()
		'WfgdmWPZ7fx'
		>>> generate_keyword(chars=string.digits)
		'15151644097'
		>>> generate_keyword(chars=string.ascii_letters, k_length=3)
		'RIF'
	"""

	# set default for chars and k_length if they are not defined
	if not chars:
		chars = string.ascii_letters+string.digits
	if not k_length:
		k_length = random.randint(8,12)

	return ''.join(random.choice(chars) for x in range(k_length))


def convert_into_seconds(duration, unit):
	"""
	Convert given duration and unit into seconds.

	Args:
		duration (int): duration
		unit (str): acronym for duration unit, 
					use: ``m`` - *month*, ``d`` - *day*, ``h`` - *hour*, ``min`` - *minute*

	Returns:
		int: converted duration in seconds

	Examples:
		>>> convert_into_seconds(2,'m') # month
		5184000
		>>> convert_into_seconds(2,'d') # day
		172800
		>>> convert_into_seconds(2,'h') # hour
		7200
		>>> convert_into_seconds(2,'min') # minute
		120
	
	"""
	if unit == 'm':
		today = date.today()
		deadline = today.replace(month=today.month+duration)
		n_days = abs(deadline - today).days
		return convert_into_seconds(duration=n_days, unit='d')
	elif unit == 'd':
		return duration * 24 * 60 * 60
	elif unit == 'h':
		return duration * 60 * 60
	elif unit == 'min':
		return duration * 60
