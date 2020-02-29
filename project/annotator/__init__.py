# -*- coding: utf-8 -*-
"""
*Subpackage* ``project.annotator``

This subpackage defines Annotator-System for annotators to annotate datas.

Main functions:
	* Login 
	* View all batches
	* Annotate batch

Two :bp:`Blueprints <blueprints>` define two annotator systems:
	* Local: at ``/annotator``
	* With `Mechanical Turk <https://www.mturk.com/>`__: at ``/mturk``
"""

from flask import Blueprint

annotator_app = Blueprint('annotator',__name__, url_prefix='/annotator')
hit_app = Blueprint('mturk', __name__, url_prefix='/mturk')

from . import account, views, annotation