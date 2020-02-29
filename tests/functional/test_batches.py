
#################################################
# Functional Tests to submit an annotated batch #
#################################################

def test_batch(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN a logged-in annotator wants to start the annotation on a batch, 
	e.g. '/annotator/test/batch-1' page is requested (GET)
	THEN check if it is redirected to the right route:
		1. the response is valid -> it is redirected to the page of batch 1
		2. it renders the right template 
		   (template 'templates/annotator/batch.html' has page title 'BATCH 1')
		3. the question(s) is rendered as well
		4. 2 Buttons Save and Submit are rendered as well
	"""
	test_client.post('/annotator',
					 data=dict(keyword='ax7832ljf', name='jung'),
					 follow_redirects=True)

	response = test_client.get('/annotator/test/batch-1')
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"BATCH 1" in response.data
	# 3.
	assert b"A, B, C, D" in response.data
	assert b'Choose the item which is, in your opinion, likely to be <strong>"BEST"</strong>' in response.data
	assert b'Choose the item which is, in your opinion, likely to be <strong>"WORST"</strong>' in response.data
	# 4.
	assert b"Submit" in response.data
	assert b"Save" in response.data

def test_submit_invalid_batch(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN a logged in annotator submits an annotation of a tuple with the same answer for 'best' and 'worst' at e.g. '/annotator/test/batch-1' page (POST)
	THEN check if it is not redirected to any other routes due to invalid inputs:
		1. the response is valid (annotator is redirected to the project page) -> GET
		2. it renders the right template 
		(template 'templates/annotator/project.html' has page title of project name 'TEST'
		3. the error messages for each invalid fields in batch pops up
	"""
	test_client.post('/annotator',
					 data=dict(keyword='ax7832ljf', name='jung'),
					 follow_redirects=True)	

	response = test_client.post('/annotator/test/batch-1',
								data={"action":"submit", "question-1-best_item":1, "question-1-worst_item":1},
								follow_redirects=True)

	# 1.
	assert response.status_code == 200
	# 2.
	assert b"BATCH 1" in response.data
	# 3.
	assert b"Two questions for this tuple require 2 different answers" in response.data

	"""
	GIVEN a Flask application
	WHEN a logged in annotator submits an annotation with no answer on the e.g. '/annotator/test/batch-1' page (POST)
	THEN check if:
		1. the response is valid (annotator is redirected to the project page) -> GET
		2. it renders the right template 
		(template 'templates/annotator/project.html' has page title of project name 'TEST'
		3. the error messages for each invalid fields in batch pops up
	"""	
	response = test_client.post('/annotator/test/batch-1',
								data={"action":"submit"},
								follow_redirects=True)

	# 1.
	assert response.status_code == 200
	# 2.
	assert b"BATCH 1" in response.data
	# 3.
	assert b"Choose one item!" in response.data

def test_submit_valid_batch(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN a logged in annotator submits a valid annotation on the e.g. '/annotator/test/batch-1' page (POST)
	THEN check if is redirected to the right route:
		1. the response is valid (annotator is redirected to the project page) -> GET
		2. it renders the right template 
		(template 'templates/annotator/project.html' has page title of project name 'TEST'
		3. a message from Admin about a successfully submitted batch pops up
	"""
	test_client.post('/annotator',
					 data=dict(keyword='ax7832ljf', name='jung'),
					 follow_redirects=True)

	response = test_client.post('/annotator/test/batch-1',
								data={"action":"submit", "question-1-best_item":'1', "question-1-worst_item":'3'}, 
								follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"TEST" in response.data
	# 3.
	assert b"Admin" in response.data
	assert b"Batch 1 successfully submitted!" in response.data

def test_resubmit_same_batch(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN a logged in annotator submits an annotation again for a submitted batch (no matter if it is valid or not)
		at e.g. '/annotator/test/batch-1' page (POST)
	THEN check if it is redirected to the right route:
		1. the response is valid (annotator is redirected to the project page) -> GET
		2. it renders the right template 
		(template 'templates/annotator/project.html' has page title of project name 'TEST'
		3. a message from Admin that this batch is already submitted pops up
	"""
	test_client.post('/annotator',
					 data=dict(keyword='ax7832ljf', name='jung'),
					 follow_redirects=True)

	response = test_client.post('/annotator/test/batch-1',
								data={"action":"submit", "question-1-best_item":'1', "question-1-worst_item":'3'}, 
								follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"TEST" in response.data
	# 3.
	assert b"Admin" in response.data
	assert b"Batch 1 already submitted!" in response.data


