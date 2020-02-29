
#################################################################
# Functional Tests to validate user registration and user login #
#################################################################

def test_user_signup(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/user/signup' page is requested (GET)
	THEN check if it is redirected to the right route:
		1. the response is valid
		2. it renders the right template 
		   (template 'templates/user/signup.html' has page title 'SIGNUP')
		3. all fields in login form are rendered as well
		4. Button Sign up is rendered
	"""
	response = test_client.get('/user/signup')
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"SIGNUP" in response.data
	# 3.
	assert b"username" in response.data
	assert b"email" in response.data
	assert b"password" in response.data
	# 4.
	assert b"Sign up" in response.data

def test_valid_signup(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN a new user signs up on the '/user/signup' page (POST) with a valid username and email
	THEN check if it is redirected to the right route:
		1. the response is valid (user is redirected to the user homepage) -> GET
		2. it renders the right template 
		(template 'templates/user/index.html' has page title of 'User - Homepage'
		3. a message from Admin about new user pops up
	"""
	response = test_client.post('/user/signup',
								data=dict(username='jung2', email='abcd@abc.de', password='12345679'),
								follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"User - Homepage" in response.data
	# 3.
	assert b"Admin" in response.data
	assert b"New user has been created" in response.data

def test_invalid_username_signup(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN a user wants to sign up on the '/user/signup' page (POST) with an existing username
	THEN check if it is not redirected to any other routes due to invalid inputs:
		1. the response is valid (GET) -> it stays at '/user/signup'
		2. it renders the right template 
		   (template 'templates/user/signup.html' has page title 'SIGNUP')
		3. the error message on username-field pops up
	"""
	response = test_client.post('/user/signup',
								data=dict(username='jung', email='abcde@abc.de', password='abcdefghij'),
								follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"SIGNUP" in response.data
	# 3.
	assert b"Username already exists! You can log in" in response.data

	"""
	GIVEN a Flask application
	WHEN a user wants to sign up on the '/user/signup' page (POST) with a username that has special character or space
	THEN check if:
		1. the response is valid (GET) -> it stays at '/user/signup'
		2. it renders the right template 
		   (template 'templates/user/signup.html' has page title 'SIGNUP')
		3. the error message on username-field pops up
	"""
	response = test_client.post('/user/signup',
								data=dict(username='jung-1', email='abcdef@abc.de', password='abcdefghij'),
								follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"SIGNUP" in response.data
	# 3.
	assert b"Username is not allowed to have space or special characters!" in response.data

	"""
	GIVEN a Flask application
	WHEN a user wants to sign up on the '/user/signup' page (POST) with a username that does not meet the length requirement
	THEN check if:
		1. the response is valid (GET) -> it stays at '/user/signup'
		2. it renders the right template 
		   (template 'templates/user/signup.html' has page title 'SIGNUP')
		3. the error message on username-field pops up
	"""
	response = test_client.post('/user/signup',
								data=dict(username='jun', email='abcdef@abc.de', password='abcdefghij'),
								follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"SIGNUP" in response.data
	# 3.
	assert b"Username must be between 4 and 15 characters long." in response.data

def test_invalid_email_signup(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN a user wants to sign up on the '/user/signup' page (POST) with an existing email
	THEN check if it is not redirected to any other routes due to invalid inputs:
		1. the response is valid (GET) -> it stays at '/user/signup'
		2. it renders the right template 
		   (template 'templates/user/signup.html' has page title 'SIGNUP')
		3. the error message on email-field pops up
	"""
	response = test_client.post('/user/signup',
								data=dict(username='maryna', email='abc@abc.de', password='abcdefghij'),
								follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"SIGNUP" in response.data
	# 3.
	assert b"Email already exists! Use another email if you want to be a new user" in response.data

	"""
	GIVEN a Flask application
	WHEN a user wants to sign up on the '/user/signup' page (POST) with an email that does not meet the format of an email
	THEN check if:
		1. the response is valid (GET) -> it stays at '/user/signup'
		2. it renders the right template 
		   (template 'templates/user/signup.html' has page title 'SIGNUP')
		3. the error message on username-field pops up
	"""
	response = test_client.post('/user/signup',
								data=dict(username='jung234', email='abc@dede', password='abcdefghij'),
								follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"SIGNUP" in response.data
	# 3.
	assert b"Invalid email" in response.data

def test_invalid_password_signup(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN a user wants to sign up on the '/user/signup' page (POST) with a password that does not meet the length requirement
	THEN check if it is not redirected to any other routes due to invalid inputs:
		1. the response is valid (GET) -> it stays at '/user/signup'
		2. it renders the right template 
		   (template 'templates/user/signup.html' has page title 'SIGNUP')
		3. the error message on password-field pops up
	"""
	response = test_client.post('/user/signup',
								data=dict(username='jung234', email='abcdef@abc.de', password='abc'),
								follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"SIGNUP" in response.data
	# 3.
	assert b"Password must be between 8 and 80 characters long." in response.data

def test_user_login(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/user/login' page is requested (GET)
	THEN check if it is redirected to the right route:
		1. the response is valid
		2. it renders the right template 
		   (template 'templates/user/login.html' has page title 'LOGIN')
		3. all fields in login form are rendered as well
		4. Button Login is rendered
	"""
	response = test_client.get('/user/login')
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"LOGIN" in response.data
	# 3.
	assert b"username" in response.data
	assert b"password" in response.data
	assert b"remember" in response.data
	# 4.
	assert b"Login" in response.data

def test_valid_login_logout(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN a user logs in on the '/user/login' page (POST) with a valid username
	THEN check if it is redirected to the right route:
		1. the response is valid (user is redirected to the valid username page) -> GET
		2. it renders the right template 
		(template 'templates/user/profile.html' has page title of 'JUNG' as logged in username is 'jung')
	"""
	response = test_client.post('/user/login',
								data=dict(username='jung', password='12345678', remember=False),
								follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"JUNG" in response.data

	"""
	GIVEN a Flask application
	WHEN a logged in user logs out (the '/user/logout' page is requested) (GET)
	THEN check if it is redirected to the right route:
		1. the response is valid (user is redirected to the 'User - Homepage') -> GET
		2. it renders the right template 
		   (template 'templates/user/index.html' has page title 'User - Homepage')
		3. this template has the logout message from Admin
	"""
	response = test_client.get('/user/logout', follow_redirects=True)
	# 1. 	
	assert response.status_code == 200
	# 2.
	assert b"User - Homepage" in response.data
	# 3.
	assert b"Admin" in response.data
	assert b"You have logged out!" in response.data


def test_invalid_username_login(test_client, init_database):

	"""
	GIVEN a Flask application
	WHEN a user logs in on the '/user/login' page (POST) with a username that is not registered
	THEN check if it is not redirected to any other routes due to invalid inputs:
		1. the response is valid (GET) -> it stays at '/user/login'
		2. it renders the right template 
		   (template 'templates/user/login.html' has page title 'LOGIN')
		3. the error message in username-field pops up
	"""
	response = test_client.post('/user/login',
								data=dict(username='jung3', password='12345678', remember=True),
								follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"LOGIN" in response.data
	# 3.
	assert b"Invalid username! Have you signed up?" in response.data

def test_invalid_password_login(test_client, init_database):
	"""
	GIVEN a Flask application
	WHEN a user logs in on the '/user/login' page (POST) with an existing username but with wrong password
	THEN check if it is not redirected to any other routes due to invalid inputs:
		1. the response is valid (GET) -> it stays at '/user/login'
		2. it renders the right template 
		   (template 'templates/user/login.html' has page title 'LOGIN')
		3. the error message in password-field pops up
	"""
	response = test_client.post('/user/login',
								data=dict(username='jung', password='12345679', remember=True),
								follow_redirects=True)
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"LOGIN" in response.data
	# 3.
	assert b"Invalid password!" in response.data

	