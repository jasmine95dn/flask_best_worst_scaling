'''
Unit Tests for models.py
'''

def test_new_user(new_user):
	"""
	GIVEN a User model
	WHEN a new User is created
	THEN check 
		1. if username, email, password are defined correctly
		2. if password is stored as hashed password, not plaintext
		3. if get_id() returns a string in form 'user:<user_id>'
	"""
	### 1.
	assert new_user.username == 'jung'
	assert new_user.email == 'abc@abc.de'
	assert new_user.password != '12345678'

	### 2.
	assert new_user.check_password('12345678')
	assert not new_user.check_password('12345679')

	### 3.
	assert new_user.get_id() == "user:12"

def test_new_annotator(new_annotator):
	"""
	GIVEN an Annotator model
	WHEN a new Annotator is created
	THEN check 
		1. if keyword is stored correctly
		2. if get_id() returns a string in form 'annotator:<annotator_id>'
	"""
	### 1.
	assert new_annotator.keyword == 'ax7832ljf'

	### 2.
	assert new_annotator.get_id() == "annotator:3"

def test_new_project(new_user, new_project, new_batch, new_tuple, new_item, new_annotator, new_data):
	"""
	GIVEN an existing User
	WHEN this User uploads a new Project and choose option 1 with local system
	THEN check
		1. if all field are stored correctly
		2. if all relationships are defined correctly
	"""
	### 1.
		## table Project
	assert new_project.name == 'test'
	assert new_project.description == 'this is a test'
	assert new_project.anno_number == 5
	assert new_project.best_def == 'best'
	assert new_project.worst_def == 'worst'
	assert new_project.n_items == 10
	assert new_project.p_name == 'test'
	assert not new_project.mturk

		## table Batch
	assert new_batch.size == 1

		## table Tuple - no extra information, so no test
		## table Item
	assert new_item.item == 'A'

		## table Data
	assert new_data.best_id == 1
	assert new_data.worst_id == 2

	### 2.
		## new_user-new_project has one-to-many relationship
	new_project.user = new_user
	assert new_project in new_user.projects

		## new_project-new_batch has one-to-many relationship
	new_batch.project = new_project
	assert new_batch in new_project.batches

		## new_tuple-new_items has many-to-many relationship
	new_tuple.items.append(new_item)
	assert new_item in new_tuple.items
	assert new_tuple in new_item.tuples

		## new_project-new_annotator has one-to-many relationship
	new_annotator.project = new_project
	assert new_annotator in new_project.annotators

		## new_annotator-new_data has one-to-many relationship
	new_data.annotator = new_annotator
	assert new_data in new_annotator.datas

		## new_tuple-new_data has one-to-many relationship
	new_data.tuple_ = new_tuple
	assert new_data in new_tuple.datas

		## new_annotator-new_batch has many-to-many relationship
	new_annotator.batches.append(new_batch)
	assert new_batch in new_annotator.batches
	assert new_annotator in new_batch.annotators
	
def test_new_project_mturk(new_project_mturk, new_batch_mturk):
	"""
	GIVEN an existing User
	WHEN this User uploads a new Project and choose option 2 with Mechanical Turk
	THEN check
		1. if all field are stored correctly
		2. this works the same like test_new_project() -> no extra test
	"""
	### 1.
		## table Project
	assert new_project_mturk.name == 'test'
	assert new_project_mturk.description == 'this is a test'
	assert new_project_mturk.anno_number == 5
	assert new_project_mturk.best_def == 'best'
	assert new_project_mturk.worst_def == 'worst'
	assert new_project_mturk.n_items == 10
	assert new_project_mturk.p_name == 'test'
	assert new_project_mturk.mturk

		## table Batch
	assert new_batch_mturk.size == 1
	assert new_batch_mturk.keyword == 'ax7832ljf'
	assert new_batch_mturk.hit_id == 'AID12897679'

