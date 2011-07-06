from flask import *

from flaskext.sqlalchemy import SQLAlchemy
from flaskext.wtf import *
from flaskext.markdown import Markdown
from datetime import datetime, timedelta
from hashlib import sha512, md5
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///betatest.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'aio3ujhrsdflncm239mlehasudkj<bkm'
db = SQLAlchemy(app)
Markdown(app, safe_mode="escape")

from betatest.filters import *
from betatest.models import *
from betatest.usersession import *
from betatest.controllers import *

def setupGlobals(sender):
    g.usersession = usersession

request_started.connect(setupGlobals)
