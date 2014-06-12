import os
from filters import *
from flask import Flask, Markup
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
#from flask.ext.migrate import Migrate
from sqlalchemy_utils import create_database, database_exists
from flask.ext.codemirror import CodeMirror

app = Flask(__name__)
app.config.from_object('config')
app.config['CODEMIRROR_LANGUAGES'] = ['python','php','html']
app.config['CODEMIRROR_THEME'] = 'eclipse'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',None)
codemirror = CodeMirror(app)

db = SQLAlchemy(app)


app.jinja_env.filters['date'] = date
app.jinja_env.filters['date_pretty'] = date_pretty
app.jinja_env.filters['datetime'] = datetime
app.jinja_env.filters['pluralize'] = pluralize
app.jinja_env.filters['month_name'] = month_name
app.jinja_env.filters['markdown'] = markdown


#migrate = Migrate(app, db)
manager = Manager(app)

from app import models
from app import views

