# -*- coding: utf-8 -*-
"""
Helper Functions
*******************


*Module* ``project.annotator.helpers``

This module defines some helper functions to deal with problems of each subroute
inside of the Annotator-System.

"""

def batches_list(project='batch', n_batches=5):
	"""
	Create buttons corresponding to number of batches inside the given project.

	Args:
		project (str): name of the project, *default:* ``batch``
		n_batches (int): number of batches inside this project, *default:* ``5``

	Returns:
		list: list of tuples ``(project, batch_id, batch_name)``

	Example:
		>>> batches_list()
		[('batch', 1, 'Batch 1'), ('batch', 2, 'Batch 2'), ('batch', 3, 'Batch 3'), ('batch', 4, 'Batch 4'), ('batch', 5, 'Batch 5')]
		>>> batches_list(project='test', n_batches=3)
		[('test', 1, 'Batch 1'), ('test', 2, 'Batch 2'), ('test', 3, 'Batch 3')]
	"""
	batches_links = [(project, i+1, f"Batch {i+1}") for i in range(n_batches)]
	return batches_links
