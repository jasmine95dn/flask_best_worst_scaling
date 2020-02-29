# -*- coding: utf-8 -*-
"""
*Module* ``project.generator``

This module provides some classes to generate and handle
different types of data during running the application. This can be used
outside the application as it works independently.

"""

from statistics import stdev
from collections import Counter
from random import shuffle, choice
from itertools import product, chain


class BaseGenerator(object):
	"""
	This class contains a base function :meth:`get_frequency` to count
	occurencies of each items in all tuples.

	Args:
		tuples (list(tuple or set or list)): list of tuples/lists/sets of items
	
	Attributes:
		frequencies (collections.Counter): container in form of a dictionary to
				save all items and frequencies inside given lists of sets

	Examples:
		>>> tuples = [('A','B','C'), ('B','C','D'),('D','A','C')]
		>>> base = BaseGenerator(tuples=tuples)
		>>> base.frequencies
		Counter({'C': 3, 'A': 2, 'B': 2, 'D': 2})

	"""

	def __init__(self, tuples):
		self.frequencies = self.get_frequency(tuples)

	def get_frequency(self, tuples):
		"""
		Count the number of tuples each item is in. 

		Args:
			tuples (list(tuple or set or list)): set of tuples

		Returns: 
			collections.Counter: frequencies of items in all tuples
		"""
		return Counter(chain(*tuples))		
		

class DataGenerator(BaseGenerator):
	"""
	Extend :class:`BaseGenerator`. Create an object of input data for the
	survey based on input file(s).

	Args:
		num_iter (int, optional): number of necessary iterations to generate 
					tuples, *default:* ``100``
		batch_size (int, optional): size of a normal batch, *default:* ``20``
		minimum (int, optional): minimum size of a batch to be formed if the
					rest items do not meet the normal size, *default:* ``5``

	Attributes:
		items (set): the unique given items
		tuples (list): list of all unique generated tuples with the best
				results after all iterations
		batches (dict): all batches prepared for questionnaire
		num_iter (int): number of necessary iterations to generate tuples,
				*default:* ``100``
		batch_size (int): size of a normal batch, *default:* ``20``
		minimum (int): minimum size of a batch to be formed if the rest
				items do not meet the normal :attr:`batch_size`, *default:* ``5``
		factor (int or float): to decide the number of tuples to be 
				generated - `n_tuples =` :attr:`factor` `* len(` :attr:`items` `)`,
				*default:* ``2`` if fewer than 10000 items 
		tuple_size (int): size of each tuple, *default:* ``4`` if fewer than 1000
				items else ``5``

	Examples:
		>>> example = open('../examples/movie_reviews_examples.txt','rb')
		>>> data = DataGenerator()
		>>> data.generate_items(example)
		>>> data.generate_data()
		>>> data.items # items read from input example
		{'interesting', 'excited', 'annoyed', 'boring', 'aggressive', 'joyful', 'fantastic', 'indifferent'}
		>>> data.tuples # tuples generated from the items (change each time calling this function)
		[['interesting', 'indifferent', 'excited', 'joyful'], ['indifferent', 'boring', 'aggressive', 'joyful'], ['interesting', 'fantastic', 'annoyed', 'indifferent'], ['joyful', 'fantastic', 'annoyed', 'indifferent'], ['fantastic', 'annoyed', 'aggressive', 'indifferent'], ['fantastic', 'boring', 'indifferent', 'joyful'], ['excited', 'boring', 'aggressive', 'interesting'], ['interesting', 'aggressive', 'annoyed', 'joyful'], ['interesting', 'fantastic', 'boring', 'aggressive'], ['excited', 'fantastic', 'indifferent', 'joyful'], ['excited', 'boring', 'annoyed', 'joyful'], ['interesting', 'fantastic', 'excited', 'indifferent'], ['excited', 'aggressive', 'annoyed', 'interesting'], ['fantastic', 'boring', 'aggressive', 'annoyed'], ['interesting', 'fantastic', 'aggressive', 'joyful'], ['excited', 'boring', 'annoyed', 'indifferent']]
		>>> data.batches # batches generated from the tuples (change each time calling this function)
		{1: [['interesting', 'indifferent', 'excited', 'joyful'], ['indifferent', 'boring', 'aggressive', 'joyful'], ['interesting', 'fantastic', 'annoyed', 'indifferent'], ['joyful', 'fantastic', 'annoyed', 'indifferent'], ['fantastic', 'annoyed', 'aggressive', 'indifferent']], 2: [['fantastic', 'boring', 'indifferent', 'joyful'], ['excited', 'boring', 'aggressive', 'interesting'], ['interesting', 'aggressive', 'annoyed', 'joyful'], ['interesting', 'fantastic', 'boring', 'aggressive'], ['excited', 'fantastic', 'indifferent', 'joyful']], 3: [['excited', 'boring', 'annoyed', 'joyful'], ['interesting', 'fantastic', 'excited', 'indifferent'], ['excited', 'aggressive', 'annoyed', 'interesting'], ['fantastic', 'boring', 'aggressive', 'annoyed'], ['interesting', 'fantastic', 'aggressive', 'joyful'], ['excited', 'boring', 'annoyed', 'indifferent']]}
		>>> data.get_frequency(data.tuples) # get frequency of each item in all generated tuples
		Counter({'indifferent': 9, 'fantastic': 9, 'interesting': 8, 'joyful': 8, 'aggressive': 8, 'annoyed': 8, 'excited': 7, 'boring': 7})
	
	"""
	def __init__(self, num_iter=100, batch_size=20, minimum=5):

		# initialize all data: items, tuples, batches
		self.items = set()
		self.tuples = []
		self.batches = {}

		# extra information
		self.num_iter = num_iter 
		self.batch_size = batch_size 
		self.minimum = minimum

		# set factor
		self.factor = 1.5 if len(self.items) > 10000 and len(self.items) %4 == 0 else 2

		# set tuple size
		self.tuple_size = 5 if len(self.items) > 1000 else 4

	def generate_tuples(self):
		"""
		Generate tuples, this is a reimplementation of `generate-BWS-tuples.pl`
		in :bws:`source code <Best-Worst-Scaling-Scripts.zip>`.

		The tuples are generated by random sampling and satisfy the following
		criteria:

			1. no two items within a tuple are identical; 
			2. each item in the item list appears approximately in the same number of tuples; 
			3. each pair of items appears approximately in the same number of tuples.

		Returns:
			list: update list of all unique generated tuples with the best results
			after all (attribute :attr:`tuples`).

		Raises:
			ValueError: if the number of :attr:`items` is fewer than :attr:`tuple_size`.

		"""
		create_key = lambda i1, i2: "%s-%s"%(i1, i2)

		# sort the items
		items = sorted(list(self.items))

		num_items = len(items)

		# check if the number of unique items is not less than 
		# the number of items requested per tuple
		if num_items < self.tuple_size:
			raise ValueError('''The number of unique items is less than the number 
										of items requested per tuple''')

		# generate tuples
		number_tuples = int(0.5 + self.factor * num_items)

		# try many iterations of different randomizations
		best_score = 0
		best_tuples = []
		iter_ = 0

		for i_iter in range(self.num_iter):
			# print('Iteration %d'%(i_iter+1))

			# generate tuples by randomly sampling without replacement
			tuples = []

			count = 1

			# make a random list of items
			random_items = items[:]
			shuffle(random_items)

			freq_pair = {}

			# set index of current item in the random list
			curr_ind = 0

			while count <= number_tuples:
				# new tuple
				new_tuple = set()

				# check if there are enough remained items in the random list for a new tuple
				if (curr_ind + self.tuple_size) <= len(random_items):
					# set a new tuple with tuple_size items in the random list 
					# starting at index curr_ind
					new_tuple = set(random_items[curr_ind:curr_ind+self.tuple_size])
					curr_ind += self.tuple_size

				# get the rest of the list
				else:

					# the number of items that we will need to get from a new random list
					need_more = self.tuple_size - len(random_items) + curr_ind

					while curr_ind < len(random_items):
						new_tuple.add(random_items[curr_ind])
						curr_ind += 1

					# generate a new random list of items
					random_items = items[:]
					shuffle(random_items)

					for curr_ind in range(need_more):
						# if there is a duplicate item, move it to the end of the list
						while random_items[curr_ind] in new_tuple:
							dup = random_items.pop(curr_ind)
							random_items.append(dup)

						new_tuple.add(random_items[curr_ind])

				# check whether this new_tuple already in the list of tuples
				if new_tuple not in tuples:
					tuples.append(new_tuple)
					count += 1
				else:
					continue
				
				# add frequencies of pairs of items
				for (item1, item2) in product(new_tuple, new_tuple):
					if item1 < item2:
						key = create_key(item1, item2)

					else: 
						key = create_key(item2, item1)

					if key in freq_pair:
						freq_pair[key] += 1
					else:
						freq_pair[key] = 1


			# calculate the two-way balance of the set of tuples
			freq_pair_values = freq_pair.values()

			# calculate the score for the set and keep the best score and the best set
			score = stdev(freq_pair_values)

			if i_iter == 0 or score < best_score:
				best_score = score
				best_tuples = tuples[:]
				# iter_ = i_iter

		# print('Choose from iteration {} with score {}'.format(iter_+1, best_score))

		self.tuples = [list(best_tuple) for best_tuple in best_tuples]

	def generate_batches(self):
		"""
		Split the whole set of tuples into batches.

		Returns:
			dict(int = list): update all batches prepared for questionnaire
					(attribute :attr:`batches`).
		
		Raises:
			ValueError: if there is no attribute :attr:`tuples`.

		"""
		if not self.tuples:
			raise ValueError('No tuples generated')

		n_tuples = len(self.tuples)

		# in case there are too few generated tuples and 
		# there is only one batch for all due to large batch size,
		# the batch size will be set to a smaller size (5)
		if n_tuples <= self.batch_size:
			self.batch_size = 5
			self.minimum = 3

		remained = n_tuples % self.batch_size

		shuffle(self.tuples)

		# divide the tuples into batches
		for count, i in enumerate(range(0, n_tuples-remained, self.batch_size)):
			self.batches[count+1] = self.tuples[i:i+self.batch_size]

		# set this batch with minimum size if it cannot fulfill the normally set batch size
		if remained >= self.minimum:
			self.batches[count+2] = self.tuples[i+self.batch_size:]

		# if the number of remained items cannot fulfill the minimum size condition, 
		# try to randomly add each of the rest tuples into the formed batches
		else:
			chosen_batches = []
			remained_tuples = self.tuples[i+self.batch_size:]

			while len(remained_tuples) > 0:
				tuple_ = remained_tuples.pop()

				# choose randomly a batch to add tuple
				i_batch = choice(list(self.batches.keys()))

				# check if all batches already have new randomly added tuples 
				# while there are still remained tuples
				while i_batch in chosen_batches:
					if len(chosen_batches) < len(self.batches):
						i_batch = choice(list(self.batches.keys()))

					# set the check to null again
					else:
						chosen_batches = []

				self.batches[i_batch].append(tuple_)
				chosen_batches.append(i_batch)

	def generate_items(self, file_name):
		"""
		Read uploaded *txt*-file. Accept only one file each time.

		Args:
			file_name (:dat-struct:`FileStorage <werkzeug.datastructures.FileStorage>` or :reader:`io.BufferedReader <io.BufferedReader>`): uploaded file

		Returns:
			list: update list of items with this file (attribute :attr:`items`).
 
		"""
		input_file = file_name.read().decode(encoding='utf-8', errors='ignore').strip()
		data = input_file.split('\n') if input_file != '' else []
		self.items = self.items.union(set(data))

	def generate_data(self):
		"""
		Generate data including tuples and batches. This method calls
		:meth:`generate_tuples` and :meth:`generate_batches`.
		"""
		self.generate_tuples()
		self.generate_batches()


class ScoreGenerator(BaseGenerator):
	"""
	Create an object to calculate the scores of given items based on annotations.

	Args:
		tuples (list): list of tuples
		best (list): list of items annotated as '**best**'
		worst (list): list of items annotated as '**worst**'

	Attributes:
		frequencies (dict or collections.Counter): frequency of each item in all tuples
		best (dict or collections.Counter): frequency of each item annotated as '**best**'
		worst (dict or collections.Counter): frequency of each item annotated as '**worst**'

	Examples:
		>>> tuples = [('A','B','C'), ('B','C','D'),('D','A','C')]
		>>> best = ['A','B','A']
		>>> worst = ['B','D','C']
		>>> generator = ScoreGenerator(tuples, best, worst)
		>>> generator.scoring()
		[('A', 1.0), ('B', 0.0), ('C', -0.3333333333333333), ('D', -0.5)]

	"""
	def __init__(self, tuples, best, worst):
		super().__init__(tuples)
		self.best = Counter(best)
		self.worst = Counter(worst)
	
	def scoring(self):
		"""
		Calculate scores of the items using formula of :orme09:`Orme 2009 <indivmaxdiff.pdf>`.

		Returns:
			list(tuple(str, float)): descendingly sorted list of tuples ``(item, score)``
			based on scores

		References:
			More about research with :bws:`Best-Worst-Scaling <>`

		"""
		scores = {}
		for item in self.frequencies:
			pos = self.best[item] if item in self.best else 0
			neg = self.worst[item] if item in self.worst else 0
			if (pos + neg) == 0:
				scores[item] = 0.0
			else:
				scores[item] = (pos - neg) / self.frequencies[item]
		return sorted(scores.items(), key=lambda item: item[1], reverse=True)
