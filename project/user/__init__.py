# -*- coding: utf-8 -*-
"""

*Subpackage* ``project.user``

This subpackage defines User-System.

Main functions:
	* Signup-Login 
	* View profiles, projects
	* Upload projects
	* Get outputs

A :bp:`Blueprint <blueprints>` defines this user system: under ``/user``

"""

from flask import Blueprint

user_app = Blueprint('user', __name__, url_prefix='/user')

from . import account, inputs, views, outputs