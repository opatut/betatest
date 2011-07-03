from flask import Flask, session, redirect, url_for, escape, request, \
        render_template

from flaskext.sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from hashlib import sha512

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///betatest.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

from betatest.models import *
from betatest.controllers import *
