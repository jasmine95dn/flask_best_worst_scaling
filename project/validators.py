# -*- coding: utf-8 -*-
"""
*Module* ``project.validators``

This module provides validators for all forms used within all systems.

	* Call the classes the same way with classes in Module :val:`wtforms.validators <>`.
	* Use functions mostly inside overwritten :form:`validate() <wtforms.form.Form.validate>`
	  or :form:`validate_<fieldname>() <wtforms.form.Form.validate>`.

"""

from wtforms.validators import ValidationError

class Unique:
	"""
	Check if input data is unique.

	Args:
		model (:db:`db.Model <flask_sqlalchemy.SQLAlchemy>`): table of database as model
		field (:db:`db.Column <flask_sqlalchemy.SQLAlchemy>`): attribute inside the table used
		message (str): message if this validator fails

	:Raises:
		:val:`ValidationError <wtforms.validators.ValidationError>` if input data is not unique.

	"""
	def __init__(self, model, field, message=u'This element already exists.'):
		self.model = model
		self.field = field
		self.message = message

	def __call__(self, form, field):
		if self.model.query.filter(self.field == field.data).first():
			raise ValidationError(self.message)


class InputValid:
	"""
	Make sure input data is valid.

	Args:
		model (:db:`db.Model <flask_sqlalchemy.SQLAlchemy>`): table of database as model
		field (:db:`db.Column <flask_sqlalchemy.SQLAlchemy>`): attribute inside the table used
		message (str): message if this validator fails

	:Raises:
		:val:`ValidationError <wtforms.validators.ValidationError>` if input data is invalid.

	"""
	def __init__(self, model, field, message=u'Invalid object'):
		self.model = model
		self.field = field
		self.message = message

	def __call__(self, form, field):
		if not self.model.query.filter(self.field==field.data).first():
			raise ValidationError(self.message)


class NotEqualTo:
	"""
	Use the same structure like default class :val:`EqualTo <built-in-validators>`.

	Make sure 2 fields are not the same.

	Args:
		other_fieldname (:db:`db.Column <flask_sqlalchemy.SQLAlchemy>`): an another 
														attribute of the table used
		message (str): message if this validator fails

	:Raises:
		:val:`ValidationError <wtforms.validators.ValidationError>` if this validator fails.	
	"""
	def __init__(self, other_fieldname, message=None):
		self.other = other_fieldname
		self.message = message

	def __call__(self, form, field):
		try:
			other = form[self.other]
		except KeyError:
			raise ValidationError(field.gettext('Invalid field name "%s"' %self.other))

		if type(field.data) == str and type(other.data) == str:
			field.data = field.data.strip()
			other.data = other.data.strip()

		if field.data == other.data:
			d = {
				'other_label': hasattr(other, 'label') and other.label.text or self.other,
				'other_name': self.other
			}
			if not self.message:
				self.message = field.gettext('Field is not allowed to be equal to %(other_name)s')
			raise ValidationError(self.message % d)


def allowed_file(filename, allowed=set(['txt'])):
	"""
	Check if uploaded file(s) have/has the right extension.

	Args:
		filename (str): name of the uploaded file
		allowed (set): list of allowed extensions, *default:* ``{'txt'}``

	Returns: 
		bool: ``True`` if this file is an allowed file, else ``False``.

	Examples:
		>>> allowed_file('example.txt')
		True
		>>> allowed_file('example.csv')
		False
		>>> allowed_file('example.csv', allowed=set(['csv']))
		True
	"""
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed
	