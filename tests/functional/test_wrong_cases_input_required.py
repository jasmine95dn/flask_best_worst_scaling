from swp.config import basedir
import os

###################################################################
# Some wrong test cases due to source code from package `wtforms` #
###################################################################

# case InputRequired with MultipleFileField
def test_upload_without_files(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN an logged-in user uploads a project on '/user/upload-project' 
		without uploading file(s) (POST)
	THEN check if:
		1. the response is valid -> user stays at '/user/upload-project' (GET)
		2. it renders the right template 
		(template 'templates/user/upload-project.html' has page title 'UPLOAD PROJECT')
		3. however, this does not reflect the right error about wtforms.validators.InputRequired.
		In fact, this error is interpreted as an empty list of file, can pass the normal validation
		on submit, reaches code block 46-49 in `project/user/inputs.py` and turns into error of 
		uploading empty files 
		(same as test_upload_empty_files() in code block 60-83 in test_projects.py)
	"""
	test_client.post('/user/login',
					data=dict(username='jung', password='12345678', remember=False),
					follow_redirects=True)
	response = test_client.post('/user/upload-project',
				data=dict(upload=None,
						  name='first 10 characters', description='this is a test about the first 10 characters',
						  anno_number=5, best_def='the best character', worst_def='the worst character'),
				follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"UPLOAD PROJECT" in response.data
	# 3.
	assert b"You uploaded only empty file(s)!" in response.data

# case InputRequired with StringField
def test_upload_no_best_def(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN an logged-in user uploads a project on '/user/upload-project' 
		without providing definition of 'best' for the project in 3 ways:
			a. best_def=None 
			b. best_def='' 
			c. not providing best_def at all
		 in 'data' of test_client.post()) (POST)
	THEN check if:
		1. the response is wrongly valid -> user is redirected to '/user/jung' (GET)
		2. it renders the wrong template.
		(template 'templates/user/profile.html' has page title of 'JUNG' as logged in username is 'jung') 
		Reason: value None of best_def is set as 'None', value '' or not given are both set as ''.
		Both of them are considered valid. As this form attribute has no other validators that can control these values,
		they are accepted as valid and this test turns into test_upload_valid_project() in `test_projects.py`.
		
	"""
	test_client.post('/user/login',
					data=dict(username='jung', password='12345678', remember=False),
					follow_redirects=True)
	### a.
	response1 = test_client.post('/user/upload-project',
				data=dict(upload=[open(os.path.join(basedir,'examples/first_10_characters_examples.txt'), 'rb')],
						  name='first 10 characters', description='this is a test about the first 10 characters',
						  anno_number=5, best_def=None, worst_def='the worst character'),
				follow_redirects=True)
	# 1.
	assert response1.status_code == 200
	# 2.
	assert b"JUNG" in response1.data

	### b.
	response2 = test_client.post('/user/upload-project',
				data=dict(upload=[open(os.path.join(basedir,'examples/first_10_characters_examples.txt'), 'rb')],
						  name='first 10 characters', description='this is a test about the first 10 characters',
						  anno_number=5, best_def='', worst_def='the worst character'),
				follow_redirects=True)
	# 1.
	assert response2.status_code == 200
	# 2.
	assert b"JUNG" in response2.data

	### c.
	response3 = test_client.post('/user/upload-project',
				data=dict(upload=[open(os.path.join(basedir,'examples/first_10_characters_examples.txt'), 'rb')],
						  name='first 10 characters', description='this is a test about the first 10 characters',
						  anno_number=5, worst_def='the worst character'),
				follow_redirects=True)
	# 1.
	assert response3.status_code == 200
	# 2.
	assert b"JUNG" in response3.data

# case InputRequired with TextAreaField
def test_upload_no_description(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN an logged-in user uploads a project on '/user/upload-project' 
		without providing project description in 3 ways:
			a. description=None 
			b. description='' 
			c. not providing description at all 
		in 'data' of test_client.post()) (POST)
	THEN check if:
		for a.
			1. the response is valid -> user stays at '/user/upload-project' (GET)
			2. it renders the right templates 
			(template 'templates/user/upload-project.html' has page title 'UPLOAD PROJECT')
			3. But pops up the wrong message, as it has an another 
			validator called Length, turns into `test_upload_short_description()` in `test_projects.py`
			 -> similar issue with code-block 9-37 (`test_upload_without_files`).
		for b,c.
			1. the response is wrongly valid -> user is redirected to '/user/jung' (GET)
			2. it renders the wrong template.
			(template 'templates/user/profile.html' has page title of 'JUNG' as logged in username is 'jung')
			-> same issue with case b. and c. from `test_upload_no_best_def`
	"""
	test_client.post('/user/login',
					data=dict(username='jung', password='12345678', remember=False),
					follow_redirects=True)
	### a.
	response1 = test_client.post('/user/upload-project',
				data=dict(upload=[open(os.path.join(basedir,'examples/first_10_characters_examples.txt'), 'rb')],
						  name='first 10 characters', description=None,
						  anno_number=5, best_def='the best character', worst_def='the worst character'),
				follow_redirects=True)
	# 1.
	assert response1.status_code == 200
	# 2.
	assert b"UPLOAD PROJECT" in response1.data
	# 3.
	assert b"Description must be at least 20 characters long."

	### b.
	response2 = test_client.post('/user/upload-project',
				data=dict(upload=[open(os.path.join(basedir,'examples/first_10_characters_examples.txt'), 'rb')],
						  name='first 10 characters', description='',
						  anno_number=5, best_def='the best character', worst_def='the worst character'),
				follow_redirects=True)
	# 1.
	assert response2.status_code == 200
	# 2.
	assert b"JUNG" in response2.data

	### c.
	response3 = test_client.post('/user/upload-project',
				data=dict(upload=[open(os.path.join(basedir,'examples/first_10_characters_examples.txt'), 'rb')],
						  name='first 10 characters', 
						  anno_number=5, best_def='the best character', worst_def='the worst character'),
				follow_redirects=True)
	# 1.
	assert response3.status_code == 200
	# 2.
	assert b"JUNG" in response3.data


# case InputRequired with PasswordField
def test_no_password_login(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN a user logs in on the '/user/login' page (POST) with an existing username
		 without password in 3 ways:
			a. password=None 
			b. password='' 
			c. not providing password at all 
		in 'data' of test_client.post()) (POST)		 

	THEN check if:
		1. the response is valid (GET) -> it stays at '/user/login'
		2. it renders the right template 
		   (template 'templates/user/login.html' has page title 'LOGIN')
		3. but pops up the wrong message, as it has an another 
		validator called `validate()`, turns it into `test_invalid_password_login()` in `test_users.py`
		 -> similar issue with code-block 9-37 (`test_upload_without_files`)
	"""
	### a.
	response1 = test_client.post('/user/login',
								data=dict(username='jung', password=None, remember=True),
								follow_redirects=True)
	# 1.
	assert response1.status_code == 200
	# 2.
	assert b"LOGIN" in response1.data
	# 3.
	assert b"Invalid password!" in response1.data

	### b.
	response2 = test_client.post('/user/login',
								data=dict(username='jung', password='', remember=True),
								follow_redirects=True)
	# 1.
	assert response2.status_code == 200
	# 2.
	assert b"LOGIN" in response2.data
	# 3.
	assert b"Invalid password!" in response2.data

	### c.
	response3 = test_client.post('/user/login',
								data=dict(username='jung', remember=True),
								follow_redirects=True)
	# 1.
	assert response3.status_code == 200
	# 2.
	assert b"LOGIN" in response3.data
	# 3.
	assert b"Invalid password!" in response3.data
