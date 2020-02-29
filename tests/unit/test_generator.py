from swp.project.generator import DataGenerator
from swp.config import basedir
import os
from itertools import chain
from collections import Counter

###############################
# Unit Tests for generator.py #
###############################

def test_generator():
	"""
	GIVEN a test-file
	WHEN this file is passed on in methods of the object DataGenerator
	THEN check:
		1. if every uploaded item is included
		2. if every item is divided in at least one tuple
		3. if items are relatively equally divided in tuples (2 conditions)
		4. if batches are relatively equally divided: 3 conditions
	"""
	
	data = DataGenerator()

	test_file = open(os.path.join(basedir,'examples/first_10_characters_examples.txt'), 'rb')
	lines = set(line.strip().decode('utf-8') for line in test_file.readlines())

	# after readlines() above, the test_file has reached the end of the line
	# seek(0) helps go back to the start position
	test_file.seek(0)
	data.generate_items(test_file)

	### 1. Every uploaded item must be included
	assert data.items == lines

	data.generate_tuples()
	
	### 2. Every item must be divided in at least one tuple
	assert set(chain(*data.tuples)) == lines

	### 3. Items must be relatively equally divided in tuples: 2 conditions
	n_items = len(data.items)

		# 1. Most of the items have the frequency in range (average frequency-2, average frequency+3)
	freq = data.get_frequency(data.tuples).values()
	avg = sum(freq) // len(freq)

	most_freq, n_items_ = tuple(chain(*Counter(freq).most_common(1)))

	assert most_freq in range(avg-2, avg+3)

		# 2. Max frequency and min frequency are in range ± 5 of average frequency
	max_freq = max(freq)
	assert max_freq in range(avg, avg+6)

	min_freq = min(freq)
	assert min_freq in range(avg-5, avg+1)

	### 4. Batches must be relatively equally divided: 3 conditions
	n_batches_size = [len(tuples) for tuples in data.batches.values()]

		# 1. Size of each batch must be in range (minimum, batch_size+minimum)
	assert all([n_ in range(data.minimum, data.batch_size+data.minimum) for n_ in n_batches_size])

		# 2. If there is no batch that has the size of range(minimum, batch_size)
	if not any([n_ in range(data.minimum, data.batch_size) for n_ in n_batches_size]):
		assert all([n_ in range(data.batch_size, data.batch_size+data.minimum) for n_ in n_batches_size])

	else:
		for i in range(len(n_batches_size)):
		# 3. Only accept one batch has the size of minimum, then other must have the same size == batch_size
			if n_batches_size[i] in range(data.minimum, data.batch_size):
				n_batches_size.pop(i)
				assert all([n_ == data.batch_size for n_ in n_batches_size])
				break


