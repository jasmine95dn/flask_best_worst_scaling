# -*- coding: utf-8 -*-
"""

*Module* ``config``

This module defines different Config objects for different servers.

"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	"""
	Base Configurations used for all servers.

	Args:
		SECRET_KEY (str): secret key of the web application
		BASE_DIR (str): base directory of the application
		SQLALCHEMY_TRACK_MODIFICATIONS (bool): whether to track modification when using SQLAlchemy, 
											*default:* ``False``
		SQLALCHEMY_DATABASE_URI (str): directory of the local SQL database, 
											*default:* ``SQLite database``
		MTURK_URL (str): endpoint of Amazon Crowdsourcing Platform, *default:* ``None``
		MTURK_SHOW_UP_URL (str): link to where the project is uploaded 
								(mainly in production environment), 
								*default:* `real page <https://requester.mturk.com/>`__
		
	Methods:
		init_app(app) : Application initialization	
	"""
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'Thisissupposedtobesecret!'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	BASE_DIR = basedir
	SQLALCHEMY_DATABASE_URI = 'sqlite:///%s'%(os.path.join(basedir, 'database.db'))
	MTURK_URL = None
	MTURK_SHOW_UP_URL = "https://requester.mturk.com/"

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	"""
	Extends :class:`Config`. Configurations used during development.

	Args:
		FLASK_ENV (str): environment of the application, *default:* ``development``
		DEBUG (bool): whether to debug during running the application, *default:* ``True``
		SQLALCHEMY_DATABASE_URI (str): SQL database used for development
		MTURK_URL (str): endpoint of Amazon Crowdsourcing Platform, used in Development environment, 
				*default:* `sandbox in us-east-1 region <https://mturk-requester-sandbox.us-east-1.amazonaws.com>`__
		AWS_ACCESS_KEY_ID (str): IAM AWS credentials - key id, *default:* ``None``
		AWS_SECRET_ACCESS_KEY (str): IAM AWS credentials - secret access key, *default:* ``None``
		MTURK_SHOW_UP_URL: link to where the project is uploaded, in development environment, 
				*default:* `Sandbox <https://workersandbox.mturk.com/>`__
	"""
	FLASK_ENV = 'development'
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
								 'sqlite:///%s'%(os.path.join(basedir, 'database-dev.db'))
	MTURK_URL = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
	AWS_ACCESS_KEY_ID = None
	AWS_SECRET_ACCESS_KEY = None
	MTURK_SHOW_UP_URL = "https://workersandbox.mturk.com/"

class TestingConfig(Config):
	"""
	Configurations used during testing.

	Args:
		DEBUG (bool): whether to debug during running the application, *default:* ``False``
		TESTING (bool): whether to set this application in testing environment, *default:* ``True``
		SQLALCHEMY_DATABASE_URI (str): SQL database used for testing
		WTF_CSRF_ENABLED (bool): whether to enable CSRF Token for different input forms in HTML, 
							*default:* ``False``
	"""
	DEBUG = False
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
								 'sqlite:///%s'%(os.path.join(basedir, 'database-test.db'))
	WTF_CSRF_ENABLED = False


config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'default': DevelopmentConfig
}
""" 
Global variable for environment configurations.
Can import this instead of configuration objects.

2 environments are available:
	* For development ``config['development']``
	* For testing ``config['testing']``

Default, ``config['default']``, is development environment.
"""