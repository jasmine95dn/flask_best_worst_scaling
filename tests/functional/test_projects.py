from swp.config import basedir
import os

####################################################
# Functional Tests to validate uploading a project #
####################################################

def test_upload_project(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN the '/user/upload-project' page is requested (GET) from a logged-in user
	THEN check if it is redirected to the right route:
		1. the response is valid
		2. it renders the right template 
		   (template 'templates/user/upload-project.html' has page title 'UPLOAD PROJECT')
		3. all fields in ProjectInformationForm are rendered
	"""
	test_client.post('/user/login',
								data=dict(username='jung', password='12345678', remember=False),
								follow_redirects=True)
	response = test_client.get('/user/upload-project')
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"UPLOAD PROJECT" in response.data
	# 3.
	assert b"Name of this project" in response.data
	assert b"Number of expected annotators for this project" in response.data
	assert b"Upload file(s) of items (.txt)" in response.data
	assert b"Description of this project" in response.data
	assert b"What does \'best\' literally mean in this project?" in response.data
	assert b"What does \'worst\' literally mean in this project?" in response.data
	assert b"Upload project on Mechanical Turk Platform?" in response.data

def test_upload_file_no_required_extensions(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN an logged-in user uploads only files on '/user/upload-project' that don't have the required extensions (POST)
	THEN check if it is not redirected to any other routes due to invalid inputs:
		1. the response is valid  -> user stays at '/user/upload-project' (GET)
		2. it renders the right template 
		(template 'templates/user/upload-project.html' has page title 'UPLOAD PROJECT')
		3. error message on upload-field pops up
	"""	
	test_client.post('/user/login',
					data=dict(username='jung', password='12345678', remember=False),
					follow_redirects=True)
	response = test_client.post('/user/upload-project',
				data=dict(upload=[open(os.path.join(basedir,'examples/first_10_characters_examples'), 'rb')],
						  name='first 10 characters again', description='this is an another test about the first 10 characters',
						  anno_number=5, best_def='the best character', worst_def='the worst character'),
				follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"UPLOAD PROJECT" in response.data
	# 3.
	assert b"No txt file(s)" in response.data

def test_upload_empty_files(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN an logged-in user uploads only empty valid txt-files on '/user/upload-project' (POST)
	THEN check if it is not redirected to any other routes due to invalid inputs:
		1. the response is valid  -> user stays at '/user/upload-project' (GET)
		2. it renders the right template 
		(template 'templates/user/upload-project.html' has page title 'UPLOAD PROJECT')
		3. error message on upload-field pops up
	"""	
	test_client.post('/user/login',
					data=dict(username='jung', password='12345678', remember=False),
					follow_redirects=True)
	response = test_client.post('/user/upload-project',
				data=dict(upload=[open(os.path.join(basedir,'examples/empty_example.txt'), 'rb')],
						  name='first 10 characters again', description='this is an another test about the first 10 characters',
						  anno_number=5, best_def='the best character', worst_def='the worst character'),
				follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"UPLOAD PROJECT" in response.data
	# 3.
	assert b"You uploaded only empty file(s)!" in response.data

def test_upload_few_items(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN an logged-in user uploads valid txt-files on '/user/upload-project' but all of items are fewer than 5 (POST)
	THEN check if it is not redirected to any other routes due to invalid inputs:
		1. the response is valid  -> user stays at '/user/upload-project' (GET)
		2. it renders the right template 
		(template 'templates/user/upload-project.html' has page title 'UPLOAD PROJECT')
		3. error message on upload-field pops up
	"""	
	test_client.post('/user/login',
					data=dict(username='jung', password='12345678', remember=False),
					follow_redirects=True)
	response = test_client.post('/user/upload-project',
				data=dict(upload=[open(os.path.join(basedir,'examples/example_fewer_5.txt'), 'rb')],
						  name='first 10 characters again', description='this is an another test about the first 10 characters',
						  anno_number=5, best_def='the best character', worst_def='the worst character'),
				follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"UPLOAD PROJECT" in response.data
	# 3.
	assert b"There are fewer than 5 items!" in response.data

def test_upload_same_best_worst_def(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN an logged-in user fills every required field on '/user/upload-project' 
		but set the definition for best and worst are the same (POST)
	THEN check if it is not redirected to any other routes due to invalid inputs:
		1. the response is valid  -> user stays at '/user/upload-project' (GET)
		2. it renders the right template 
		(template 'templates/user/upload-project.html' has page title 'UPLOAD PROJECT')
		3. error messages on best_def-field and worst_def-field pop up
	"""	
	test_client.post('/user/login',
					data=dict(username='jung', password='12345678', remember=False),
					follow_redirects=True)
	response = test_client.post('/user/upload-project',
				data=dict(upload=[open(os.path.join(basedir,'examples/first_10_characters_examples.txt'), 'rb')],
						  name='first 10 characters again', description='this is an another test about the first 10 characters',
						  anno_number=5, best_def='the best character', worst_def='the best character'),
				follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"UPLOAD PROJECT" in response.data
	# 3.
	assert b"Both definitions are not the same!" in response.data

def test_upload_short_description(test_client, init_database):		
	"""
	GIVEN a Flask application
	WHEN an logged-in user uploads a project on '/user/upload-project' 
		with a very short project description (fewer than 10 characters) (POST)
	THEN check if it is not redirected to any other routes due to invalid inputs:
		1. the response is valid -> user stays at '/user/upload-project' (GET)
		2. it renders the right template 
		(template 'templates/user/upload-project.html' has page title 'UPLOAD PROJECT')
		3. error message
	"""
	test_client.post('/user/login',
					data=dict(username='jung', password='12345678', remember=False),
					follow_redirects=True)
	response = test_client.post('/user/upload-project',
				data=dict(upload=None,
						  name='first 10 characters', description='Nothing here',
						  anno_number=5, best_def='the best character', worst_def='the worst character'),
				follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"UPLOAD PROJECT" in response.data
	# 3.
	assert b"Description must be at least 20 characters long."

def test_upload_no_anno_number(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN an logged-in user uploads a project on '/user/upload-project' 
		without providing number of expected annotators for the project (POST)
	THEN check if it is not redirected to any other routes due to invalid inputs:
		1. the response is valid -> user stays at '/user/upload-project' (GET)
		2. it renders the right template 
		(template 'templates/user/upload-project.html' has page title 'UPLOAD PROJECT')
	"""
	test_client.post('/user/login',
					data=dict(username='jung', password='12345678', remember=False),
					follow_redirects=True)
	response = test_client.post('/user/upload-project',
				data=dict(upload=[open(os.path.join(basedir,'examples/first_10_characters_examples.txt'), 'rb')],
						  name='first 10 characters', description='this is a test about the first 10 characters',
						  anno_number=None, best_def='the best character', worst_def='the worst character'),
				follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"UPLOAD PROJECT" in response.data

def test_upload_valid_project(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN an logged-in user uploads a valid project on '/user/upload-project' (POST)
	THEN check if it is redirected to the right route:
		1. the response is valid (user is redirected to the valid username page) -> GET
		2. it renders the right template 
		(template 'templates/user/profile.html' has page title of 'JUNG' as logged in username is 'jung')
	"""
	test_client.post('/user/login',
					data=dict(username='jung', password='12345678', remember=False),
					follow_redirects=True)
	response = test_client.post('/user/upload-project',
				data=dict(upload=[open(os.path.join(basedir,'examples/first_10_characters_examples.txt'), 'rb')],
						  name='first 10 characters', description='this is a test about the first 10 characters',
						  anno_number=5, best_def='the best character', worst_def='the worst character'),
				follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"JUNG" in response.data

	