###########################################
# Functional Tests to test all home pages #
###########################################

def test_home_page(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/' page is requested (GET)
	THEN check if is redirected to the right route:
		1. if the response is valid
		2. if it renders the right template 
		   (template **templates/start.html** has page title 'Homepage')
	"""
	response = test_client.get('/')
	assert response.status_code == 200
	assert b"Homepage" in response.data
	assert b"""This is a simple website using """ in response.data

def test_user_homepage(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/user' page is requested (GET)
	THEN check if it is redirected to the right route:
		1. the response is valid
		2. it renders the right template 
		   (template 'templates/user/index.html' has page title 'User - Homepage')
		3. 2 Buttons Sign up and Login are rendered as well
	"""
	response = test_client.get('/user')
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"User - Homepage" in response.data
	# 3.
	assert b"Sign up" in response.data
	assert b"Login" in response.data

def test_annotator_homepage(test_client):
	"""
	GIVEN a Flask application
	WHEN the '/annotator' page is requested (GET)
	THEN check if it is redirected to the right route:
		1. the response is valid
		2. it renders the right template 
		   (template 'templates/annotator/index.html' has page title 'Annotator - Main page')
		3. all fields for form log in are rendered
		4. Button Confirm identity is rendered
	"""
	response = test_client.get('/annotator')
	# 1.
	assert response.status_code == 200
	# 2.
	assert b"Annotator - Main page" in response.data
	# 3.
	assert b"Keyword as annotator" in response.data
	assert b"Specify your name" in response.data	
	# 4.
	assert b"Confirm identity"
