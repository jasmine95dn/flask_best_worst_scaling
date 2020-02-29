import pytest

#######################################
# Functional Tests to annotator login #
#######################################

def test_valid_annotator(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN an annotator uses a keyword on the '/user/signup' page (POST) 
	which is never used from other annotators
	THEN check if it is redirected to the right route:
		1. the response is valid 
		-> annotator is redirected to the project homepage '/annotator/test' (GET)
		2. it renders the right template 
		(template 'templates/annotator/project.html' has page title of project name 'TEST'
		3. it is redirected correctly to the project page of annotator system, 
		it has the buttons to all batches for annotation
	"""
	response = test_client.post('/annotator',
								data=dict(keyword='ax7832ljf', name='jung'),
								follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"TEST" in response.data
	# 3.
	assert b"Batch 1" in response.data

	"""
	GIVEN a Flask application
	WHEN an annotator uses a keyword on the '/user/signup' page (POST) 
	that he has already used and can type in his pseudoname (self defined) again
	THEN check if is redirected to the right route:
		1. the response is valid 
		-> annotator is redirected to the project homepage '/annotator/test' (GET)
		2. it renders the right template 
		(template 'templates/annotator/project.html' has page title of project name 'TEST'
		3. it is redirected correctly to the project page of annotator system, 
		it has the buttons to all batches for annotation
	"""
	response = test_client.post('/annotator',
								data=dict(keyword='kjd8f9s879', name='sanaz'),
								follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"TEST" in response.data
	# 3.
	assert b"Batch 1" in response.data

def test_invalid_keyword(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN an annotator types in a wrong keyword on the '/annotator' page (POST)
	THEN check if it is not redirected to any other routes due to invalid inputs:
		1. the response is valid -> annotator stays at main page at '/annotator' (GET)
		2. it renders the right template 
		(template 'templates/annotator/index.html' has page title of 'Annotator - Main page'
		3. an error message on keyword-field pops up
	"""
	response = test_client.post('/annotator',
								data=dict(keyword='kjd8f9s87', name='sanaz'),
								follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"Annotator - Main page" in response.data
	# 3.
	assert b"Invalid keyword!" in response.data

def test_invalid_name(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN an annotator types in the right keyword but specifies the wrong name on the '/user/signup' page (POST)
	as this keyword is used from an another user
	THEN check if it is not redirected to any other routes due to invalid inputs:
		1. the response is valid (annotator stays on the main page) -> GET
		2. it renders the right template 
		(template 'templates/annotator/index.html' has page title of 'Annotator - Main page'
		3. an error message on name-field pops up
	"""
	response = test_client.post('/annotator',
								data=dict(keyword='kjd8f9s879', name='maryna'),
								follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"Annotator - Main page" in response.data
	# 3.
	assert b"""This name is not used for this keyword! Have you logged in with this keyword before? If not, someone has already used it!""" in response.data

