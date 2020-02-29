# -*- coding: utf-8 -*-
"""
Inputs
#################

*Module* ``project.user.inputs``

This module defines routes to manage input new inputs of projects from users.

"""

import re, boto3, string
from flask import render_template, redirect, url_for, Response, current_app
from flask_login import login_required, current_user
from . import user_app
from .forms import ProjectInformationForm
from .helpers import upload_file, generate_keyword, convert_into_seconds
from .. import db
from ..models import Project, Annotator, Batch, Tuple, Item


# User - Upload project
@user_app.route('/upload-project', methods=['GET','POST'])
@login_required 
def upload_project():
	"""
	Provide information of a new project from user at ``/user/upload-project``.

	Returns:
		user profile page at ``/user/<some_name>`` if new valid project is submitted.
		
	Note:
		Upload project on Mechanical Turk Platform or use local annotator system.

	Error:
		Error message emerges if there are invalid fields or there is no logged in user.
	"""
	
	# information about project
	project_form = ProjectInformationForm()

	if project_form.validate_on_submit():
		
		# get data from uploaded file
		data = upload_file(project_form.upload.data)

		# check if user uploaded empty validated file(s)
		if not data:
			project_form.upload.errors.append(u'You uploaded only empty file(s)!')
			return render_template('user/upload-project.html', form=project_form, 
									name=current_user.username)

		# check if user uploaded too few items
		elif data == 1:
			project_form.upload.errors.append(u'There are fewer than 5 items!')
			return render_template('user/upload-project.html', form=project_form, 
									name=current_user.username)

		# get project name
		# if no name was given, then this project has the name 'project - <project-id>'
		if not project_form.name.data:
			name = 'project-%d'%(len(Project.query.all()))
		else:
			name = project_form.name.data.strip()

		# add link to project page for user to view project information
		p_name = ("%s"%(re.sub('[^\w]+', '-', name))).strip('-').strip('_')
		
		# if this name exists already (more than one user have the same project name)
		if Project.query.filter_by(name=name).first():
			
			# create link for this new project by adding its id
			p_name = '%s-%d'%(p_name,len(Project.query.all()))

			# rename the project of this user uses the same name for more than 
			# one of his project (which rarely happens)
			while Project.query.filter_by(name=name, user=current_user).first():
				name = '%s (%d)'%(name,len([project for project in current_user.projects \
											 if project.name==name]))

		# if name of the project is unique but the link exists (p_name), 
		# hope this will happen only once, but to make sure
		while Project.query.filter_by(p_name=p_name).first():
			p_name = '%s-%d'%(p_name,len(Project.query.all()))			
			

		# add new project 
		current_project = Project(name=name, description=project_form.description.data, \
				anno_number=project_form.anno_number.data, \
				best_def=project_form.best_def.data, worst_def=project_form.worst_def.data, \
				n_items=len(data.items), user=current_user, p_name=p_name, \
				mturk=project_form.mturk.data)

		# user wants to upload this project on Mechanical Turk Market
		if project_form.mturk.data:

			# use the aws_access_key_id and aws_secret_access_key given from user
			# if this is not found in configuration
			aws_access_key_id = current_app.config['AWS_ACCESS_KEY_ID'] \
											if current_app.config['AWS_ACCESS_KEY_ID'] \
											 else project_form.aws_access_key_id.data

			aws_secret_access_key = current_app.config['AWS_SECRET_ACCESS_KEY'] \
											if current_app.config['AWS_SECRET_ACCESS_KEY'] \
											 else project_form.aws_secret_access_key.data

			# check if the user uses default values which never exists
			check = []
			if aws_access_key_id == project_form.aws_access_key_id.default:
				project_form.aws_access_key_id.errors.append("""You must specify your own 
													aws_access_key_id, default does not exist!""")
				check.append(True)
			if aws_secret_access_key == project_form.aws_secret_access_key.default:
				project_form.aws_secret_access_key.errors.append("""You must specify your own 
												 aws_secret_access_key, default does not exist!""")
				check.append(True)
			if any(check):
				return render_template('user/upload-project.html', form=project_form, 
												name=current_user.username)

			mturk = boto3.client(service_name='mturk',
				   aws_access_key_id = aws_access_key_id,
				   aws_secret_access_key = aws_secret_access_key,
				   region_name='us-east-1',
				   endpoint_url = current_app.config['MTURK_URL'])

			# define endpoint to a HIT using generated hit_id 
			hit_ids = set()
			hit_code = generate_keyword(chars=string.ascii_letters, k_length=3)

		# user wants to choose annotators themselves (they want to use our local system)
		else:
			# add keywords for annotators in local system
			for num_anno in range(project_form.anno_number.data):
				new_keyword = generate_keyword()

				# make sure the new created keyword is never used for any annotator of any project
				while Annotator.query.filter_by(keyword=new_keyword).first():
					new_keyword = generate_keyword()

				# add new key word 
				Annotator(keyword=new_keyword, project=current_project)

		# add batches, tuples and items
		for i, tuples_ in data.batches.items():

			# create keyword for each batch to upload this project on Mechanical Turk Market
			if project_form.mturk.data:
				new_keyword = generate_keyword()

				# make sure the new created keyword is never used for any batch of any project
				while Batch.query.filter_by(keyword=new_keyword).first():
					new_keyword = generate_keyword()

				# create this HIT on MTurk
				# create HIT_ID for the batch in local system (has nothing to do with HITID on MTurk)
				new_hit_id = hit_code+generate_keyword(chars=string.digits)
				while new_hit_id in hit_ids:
					new_hit_id = hit_code+generate_keyword(chars=string.digits)
				hit_ids.add(new_hit_id)

				# get url for the hit to save on corresponding one on MTurk
				url = url_for('mturk.hit', p_name=p_name, hit_id=new_hit_id, _external=True)

				# define the questions.xml template with the type box for keyword
				response = Response(render_template('questions.xml', title=project_form.name.data,
												description=project_form.description.data, url=url), 
									mimetype='text/plain')
				response.implicit_sequence_conversion = False
				question = response.get_data(as_text=True)
				
				# get information from user for creating hit on MTurk
				p_keyword = project_form.keywords.data
				p_reward = project_form.reward.data
				lifetime = convert_into_seconds(duration=project_form.lifetime.data, \
											 unit=project_form.lifetimeunit.data)
				hit_duration = convert_into_seconds(duration=project_form.hit_duration.data, \
													 unit=project_form.duration_unit.data)

				# create new hit on MTurk
				new_hit = mturk.create_hit(
				    Title = project_form.name.data, 
				    Description = project_form.description.data,
				    Keywords = p_keyword,  
				    Reward = p_reward, 
				    MaxAssignments = project_form.anno_number.data,
				    LifetimeInSeconds = lifetime, 
				    AssignmentDurationInSeconds = hit_duration, 
				    Question = question,
				    AssignmentReviewPolicy = {
				    'PolicyName':'ScoreMyKnownAnswers/2011-09-01',
				    'Parameters': [ 
				    	{'Key':'AnswerKey', 
				    	 'MapEntries':[{ 'Key':'keyword', 
				    				 	 'Values':[new_keyword]
				    				 	}]
				    	},
				        {'Key':'ApproveIfKnownAnswerScoreIsAtLeast', 
				         'Values':['1']
				        },
	                    {'Key':'RejectIfKnownAnswerScoreIsLessThan',
	                     'Values':['1']
	                    },
	                    {'Key':'RejectReason', 
	                     'Values':['''Sorry, we could not approve your submission 
	                     			as you did not type in the right keyword.''']
	                    }
				                ]
				    }
				)

			# no need to create keyword and hit_id for batch as this is for the local process
			else:
				new_keyword = new_hit_id = None

			# add new batch 
			current_batch = Batch(project=current_project, size=len(tuples_), 
													keyword=new_keyword, hit_id=new_hit_id)

			for tuple_ in tuples_:

				# add new tuple
				current_tuple = Tuple(batch=current_batch)
				
				for item in tuple_:
					
					# check if this item is already saved in the database
					if Item.query.filter_by(item=item).first():
						current_tuple.items.append(Item.query.filter_by(item=item).first())
					else:
						new_item = Item(item=item)
						current_tuple.items.append(new_item)

		db.session.commit()
		
		return redirect(url_for('user.profile', some_name=current_user.username))
		
	return render_template('user/upload-project.html', form=project_form, name=current_user.username)
