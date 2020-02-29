# -*- coding: utf-8 -*-
"""
Forms
******

*Module* ``project.annotator.forms``


This module defines forms used inside of the Annotator-System.

"""

from flask_wtf import FlaskForm
from wtforms import RadioField, PasswordField, StringField
from wtforms.validators import InputRequired
from ..validators import NotEqualTo, InputValid
from ..models import Annotator


class TupleForm(FlaskForm):
	"""
	Extend :fform:`FlaskForm <flask_wtf.FlaskForm>`.
	Define form for a tuple with two choices for **best** and **worst** item.

	Attributes:
		best_item (:field:`RadioField <wtforms.fields.RadioField>`): answer for the question
																	of best item
		worst_item (:field:`RadioField <wtforms.fields.RadioField>`): answer for the question
																	of worst item


	"""
	best_item = RadioField('Label', coerce=int, 
					validators= [InputRequired(message=u'Choose one item!'), \
								NotEqualTo('worst_item', 
								message=u'Two questions for this tuple require 2 different answers')
								])
	worst_item = RadioField('Label', coerce=int, 
					validators= [InputRequired(message=u'Choose one item!'),
								NotEqualTo('best_item', 
								message=u'Two questions for this tuple require 2 different answers')
								])


class AnnoCheckinForm(FlaskForm):
	"""
	Extend :fform:`FlaskForm <flask_wtf.FlaskForm>`. Define form for an annotator login-system.

	Attributes:
		keyword (:field:`PasswordField <wtforms.fields.PasswordField>`): keyword to log in
		name (:field:`StringField <wtforms.fields.StringField>`): pseudoname given by annotator

	"""
	keyword = PasswordField('Keyword as annotator', 
							validators=[InputRequired(message=u''), 
										InputValid(model=Annotator, field=Annotator.keyword, 
											message=u'Invalid keyword!')
										])
	name = StringField('Specify your name', validators=[InputRequired(message=u'')])

	
	def validate(self):
		"""
		Override  :form:`validate() <wtforms.form.Form.validate>`.

		Check if the person using this keyword is the first one who logged in
		by checking his given (pseudo)name.
		"""
		if not FlaskForm.validate(self):
			return False

		if Annotator.query.filter(Annotator.keyword==self.keyword.data, Annotator.name.isnot(None), Annotator.name==self.name.data).first() \
		 or Annotator.query.filter(Annotator.keyword==self.keyword.data, Annotator.name==None).first():
			return True
		self.name.errors.append(u'This name is not used for this keyword! Have you logged in with this keyword before? If not, someone has already used it!')
		return False
