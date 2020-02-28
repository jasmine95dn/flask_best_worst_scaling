from project import create_app, db
from config import config

app = create_app(config['default'])

with app.app_context():
	from project.models import *
	db.create_all()

app.run()