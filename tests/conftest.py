import pytest, os
from swp.project.models import *
from swp.project import create_app, db
from swp.config import config

#################################
# Configurations for Unit Tests #
#################################

@pytest.fixture(scope='module')
def new_user():
	user = User(username='jung', email='abc@abc.de', password='12345678')
	user.id = 12
	return user

@pytest.fixture(scope='module')
def new_project():
	project = Project(name='test', description='this is a test', \
				anno_number=5, best_def='best', worst_def='worst', \
				n_items=10, p_name='test', \
				mturk=False)
	return project

@pytest.fixture(scope='module')
def new_project_mturk():
	project = Project(name='test', description='this is a test', \
				anno_number=5, best_def='best', worst_def='worst', \
				n_items=10, p_name='test', \
				mturk=True)
	return project

@pytest.fixture(scope='module')
def new_batch():
	return Batch(size=1)

@pytest.fixture(scope='module')
def new_batch_mturk():
	return Batch(size=1, keyword='ax7832ljf', hit_id='AID12897679')

@pytest.fixture(scope='module')
def new_tuple():
	return Tuple()

@pytest.fixture(scope='module')
def new_item():
	item = Item(item='A')
	item.id = 1
	return item

@pytest.fixture(scope='module')
def new_annotator():
	annotator = Annotator(keyword='ax7832ljf')
	annotator.id = 3
	return annotator

@pytest.fixture(scope='module')
def new_data():
	data = Data(best_id=1, worst_id=2)
	return data

#######################################
# Configurations for Functional Tests #
#######################################

@pytest.fixture(scope='module')
def test_client():
	app = create_app(config['testing'])

	# Expose the Flask client
	testing_client = app.test_client()

	# Establish an application context before running the tests
	context = app.app_context()
	context.push()

	# this is where the testing happens
	yield testing_client

	# Tear down the application context after running the tests
	context.pop()

@pytest.fixture(scope='module')
def init_database(new_user, new_project, new_batch, new_tuple, new_item, new_annotator):
	# Drop if there is an existing database
	db.drop_all()

	# Create the test database with the tables
	db.create_all()

	# Insert user data
	db.session.add(new_user)

	# Insert project data into user data
	new_project.user = new_user

	# Insert batch data into project data
	new_batch.project = new_project


	# Insert tuple data into batch data
	new_tuple.batch = new_batch

	# Insert item data into tuple data
	item2 = Item(item='B')
	item2.id = 2

	item3 = Item(item='C')
	item3.id = 3

	item4 = Item(item='D')
	item4.id = 4

	new_tuple.items.extend([new_item, item2, item3, item4])

	# Insert annotator data into project data
	new_annotator.project = new_project
	annotator = Annotator(keyword='kjd8f9s879', name='sanaz', project=new_project)
	annotator.id = 2

	# Commit the changes for the users
	db.session.commit()

	# this is where the testing happens
	yield db

	# Tear down the database after running the functional tests
	db.session.remove()

