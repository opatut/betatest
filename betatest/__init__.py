from flask import *

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import *
from flask.ext.markdown import Markdown
from datetime import datetime, timedelta
from hashlib import sha512, md5
import hashlib
import re, random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///betatest.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'aio3ujhrsdflncm239mlehasudkj<bkm'
db = SQLAlchemy(app)
Markdown(app, safe_mode="escape")

def abort_reason(code, reason):
    session["abort_reason"] = reason
    abort(code)

@app.context_processor
def inject_user():
    return dict(current_user = usersession.getCurrentUser(), random = random, hashlib = hashlib)


import validators
from betatest.forms import *
from betatest.filters import *
from betatest.models import *
from betatest.usersession import *
from betatest.controllers import *
