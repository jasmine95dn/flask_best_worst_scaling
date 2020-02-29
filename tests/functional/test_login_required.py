import pytest
#############################################################
# Functional Tests to test pages requiring a logged in user #
#############################################################

@pytest.mark.parametrize("route1", ['/user/jung', '/user/jung/test', '/user/jung/test/keywords.txt',
									'/user/jung/test/report.txt', '/user/jung/test/scores.txt'])
@pytest.mark.parametrize("route2" ,['/user/upload-project'])
def test_login_required_user(test_client, route1, route2):
	"""
	GIVEN a Flask application
	WHEN a non-logged-in user tries to access the one of the routes above, which requires logged-in user 
	(profile, user project, results of the user project, and upload project)
	THEN check if:
		1. the response is valid as unaccepted (GET 302)
		2. it is redirected to the page '/user/login'
	"""
	response = test_client.get(route1)
	# 1.
	assert response.status_code == 302
	# 2.
	assert response.headers['Location'].startswith('http://localhost/user/login?next=%2Fuser%2Fjung')

	response = test_client.get(route2)
	# 1.
	assert response.status_code == 302
	# 2.
	assert response.headers['Location'].startswith('http://localhost/user/login?next=%2Fuser%2Fupload-project')


@pytest.mark.parametrize("route", ['/annotator/test', '/annotator/test/batch-1'])
def test_login_required_annotator(test_client, route):
	"""
	GIVEN a Flask application
	WHEN a non-logged-in user tries to access the one of the routes above, which requires logged-in user 
	(profile, user project, results of the user project, and upload project)
	THEN check if:
		1. the response is valid as unaccepted (GET 302)
		2. it is redirected to the page '/annotator'
	"""
	response = test_client.get(route)
	# 1.
	assert response.status_code == 302
	# 2.
	assert response.headers['Location'].startswith('http://localhost/annotator?next=%2Fannotator%2Ftest')
