# -*- coding: utf-8 -*-
"""
Outputs
##################

*Module* ``project.user.outputs``

This module defines routes to manage outputs for users.

"""

from flask import redirect, url_for, flash, Response
from flask_login import login_required, logout_user, current_user
from . import user_app
from .forms import LoginForm
from .helpers import is_not_current_user
from ..generator import ScoreGenerator
from ..models import Project, Item, Data

# User - Get Scores
@user_app.route('/<some_name>/<p_name>/scores.txt')
@login_required
def get_scores(some_name, p_name):
	"""
	Collect the annotated data, calculate the BWS-score for each item 
	and save them as ``/user/<some_name>/<p_name>/scores.txt``. 

	Args:
		some_name (str): user name 
		p_name (str): project name

	Returns:
		Items with scores in .txt-file, if at least one batch or HIT is submitted, else no result.

	Error:
		Error message emerges if user of this project is not logged in.
	"""
	# only between users in User-System, no access to an account 
	# (not currently signed in account) without providing password
	if is_not_current_user(user=current_user, current_name=some_name):
		flash(f'Your username is "{current_user.username}",\
					 you have no access to another account without password.', 'login')
		logout_user()
		return redirect(url_for('user.login', form=LoginForm()))

	current_project = Project.query.filter_by(p_name=p_name, user=current_user).first()

	tuples, best, worst = [],[],[]

	# collect annotations from annotators (Workers) from MTurk
	if current_project.mturk:
		for batch in current_project.batches:
			for tuple_ in batch.tuples:
				for data in tuple_.datas:
					tuples.append([item.id for item in data.tuple_.items])
					best.append(data.best_id)
					worst.append(data.worst_id)

	# collect annotations from annotators from local system
	else:
		for annotator in current_project.annotators:
			# get submitted batch(es) of this project by this annotator
			for batch in annotator.batches:
				for tuple_ in batch.tuples:
					data = Data.query.filter_by(annotator=annotator, tuple_=tuple_).first()
					tuples.append([item.id for item in data.tuple_.items])
					best.append(data.best_id)
					worst.append(data.worst_id)
	
	if tuples:
		scores = ScoreGenerator(tuples, best, worst).scoring()
		out = [f'{Item.query.get(key).item}\t{value}' for key, value in scores] 
		
		# return output
		return Response('\n'.join(out), mimetype='text/plain')

	else:
		return '<h2> No result yet! </h2>'


# User - Get Report
@user_app.route('/<some_name>/<p_name>/report.txt')
@login_required
def get_report(some_name, p_name):
	"""

	Collect the annotated data and save at ``/user/<some_name>/<p_name>/report.txt``.

	Args:
		some_name (str): user name 
		p_name (str): project name

	Returns:
		Report in .txt-file with all the submitted data.

	Error:
		Error message emerges if user of this project is not logged in.
	"""
	# only between users in User-System, no access to an account 
	# (not currently signed in account) without providing password
	if is_not_current_user(user=current_user, current_name=some_name):
		flash(f'Your username is "{current_user.username}", \
		 		you have no access to another account without password.', 'login')
		logout_user()
		return redirect(url_for('user.login', form=LoginForm()))

	current_project = Project.query.filter_by(p_name=p_name, user=current_user).first()

	out = []
	out.append((f'\tProject: "{current_project.name.upper()}"\t').center(30).center(120, '*'))

	# collect annotations from annotators (Workers) from MTurk
	if current_project.mturk:
		for b_id, batch in enumerate(current_project.batches):
			out.append(f'\nBatch {b_id+1}')
			for t_id, tuple_ in enumerate(batch.tuples):
				out.append(u'\tTuple %d:\t%s'%(t_id+1, 
											 ', '.join([f"{item.item}" for item in tuple_.items]) 
											   )
							)
				if len(tuple_.datas) > 0:
					for d_anno, data in enumerate(tuple_.datas):
						out.append(f"\t\tAnnotation {d_anno+1}: ")
						out.append(f"\t\t\t{current_project.best_def} - {Item.query.get(data.best_id).item}")
						out.append(f"\t\t\t{current_project.worst_def} - {Item.query.get(data.worst_id).item}\n")
				else:
					out.append('\t\tNo result yet!\n')
			out.append('#'*100)

	# collect annotations from annotators from local system
	else:
		annotators = current_project.annotators
		for b_id, batch in enumerate(current_project.batches):
			out.append(f'\nBatch {b_id+1}')
			for t_id, tuple_ in enumerate(batch.tuples):
				out.append(u'\tTuple %d:\t%s'%(t_id+1, 
											', '.join([f"{item.item}" for item in tuple_.items])
											  )
						)
				if batch.annotators:
					for annotator in batch.annotators:
						data = Data.query.filter_by(annotator=annotator, tuple_=tuple_).first()

						out.append(f"\t\tAnnotator {annotators.index(annotator)+1} - '{annotator.name}': ")
						out.append(f"\t\t\t{current_project.best_def} - {Item.query.get(data.best_id).item}")
						out.append(f"\t\t\t{current_project.worst_def} - {Item.query.get(data.worst_id).item}\n")
				else:
					out.append('\t\tNo result yet!\n')
			out.append('#'*100)

	# return output
	return Response('\n'.join(out), mimetype='text/plain')


# User - Get Keywords for annotators
@user_app.route('/<some_name>/<p_name>/keywords.txt')
@login_required
def get_keywords(some_name, p_name):
	"""
	Collect keywords for annotators and save at ``/user/<some_name>/<p_name>/keywords.txt``.

	Args:
		some_name (str): username 
		p_name (str): project name as endpoint

	Returns:
		Keywords for annotators within the project in .txt-file 
		if this project is on the local system, else no keyword 
		(this project is created on Mechanical Turk).

	Error:
		Error message emerges if user of this project is not logged in.
	"""
	# only between users in User-System, no access to an account 
	# (not currently signed in account) without providing password
	if is_not_current_user(user=current_user, current_name=some_name):
		flash(f'Your username is "{current_user.username}", you have no access to another account without password.', 'login')
		logout_user()
		return redirect(url_for('user.login', form=LoginForm()))

	current_project = Project.query.filter_by(p_name=p_name, user=current_user).first()

	if current_project.mturk:
		return '<h1> No keywords defined here </h1>'
	else:
		out = [annotator.keyword.rjust(20) for annotator in current_project.annotators]

	# return output
	return Response('\n'.join(out), mimetype='text/plain')


