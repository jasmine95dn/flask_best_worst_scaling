.. BWS documentation master file, created by
   sphinx-quickstart on Mon Feb 17 13:23:53 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Web Interface for **Best-Worst-Scaling**
=========================================

Welcome to the Project's documentation! 

This is a documentation for the source code to the web application for **Best-Worst-Scaling**. The source code includes scripts for frontend and backend.

Backend is mainly developed with `Python3.6 <https://www.python.org/downloads/release/python-369/>`__ using `Flask <https://flask.palletsprojects.com/en/1.1.x/>`__ and its extensions. The application is also integrated with Amazon Crowdsourcing Platform using its `API <https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html>`__.

For the frontend development, besides `HTML <https://www.w3schools.com/html/default.asp>`__, `CSS <https://www.w3schools.com/css/default.asp>`__, `JavaScript <https://www.w3schools.com/js/default.asp>`__ and `Bootstrap4 <https://getbootstrap.com/>`__, `Jinja2 <https://jinja.palletsprojects.com/en/2.11.x/>`__ is used for dynamic rendering of the most of the templates.

Links
-------
`Source code <https://gitlab.cl.uni-heidelberg.de/nguyen/swp>`__


Contents
---------------------

Backend
########
.. toctree::
   :maxdepth: 4

   config
   project_rst/project


Frontend
#########
.. toctree::
   :maxdepth: 3

   templates
 

Indices and tables
-------------------
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`