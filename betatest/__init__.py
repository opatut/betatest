from flask import *

from flaskext.sqlalchemy import SQLAlchemy
from flaskext.wtf import *
from datetime import datetime, timedelta
from hashlib import sha512, md5
from markdown2 import markdown as Markdown
import re

	
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///betatest.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'aio3ujhrsdflncm239mlehasudkj<bkm'
db = SQLAlchemy(app)

#define filters

@app.template_filter()
def markdown(s):
	return Markdown(s)

@app.template_filter()
def formattime(s):
	return s.strftime("%Y-%m-%d %H:%M:%S")

@app.template_filter()
def humantime(s):
	diff = datetime.utcnow() - s
	if(diff.seconds < 10):
		return "just now"
	elif(diff.seconds < 60):
		return str(diff.seconds) + " second" + ("s" if diff.seconds > 1 else "") + " ago"
	mins = (diff.seconds - diff.seconds % 60) / 60
	if(mins < 60):
		return str(mins) + " minute" + ("s" if mins > 1 else "") + " ago"
	hours = (mins - mins % 60) / 60
	if(hours < 24):
		return str(hours) + " hour" + ("s" if hours > 1 else "") + " ago"
	if(diff.days < 14):
		return str(diff.days) + " day" + ("s" if diff.days > 1 else "") + " ago"
	weeks = (diff.days - diff.days % 7) / 7
	if(weeks <= 4):
		return str(weeks) + " week" + ("s" if weeks > 1 else "") + " ago"
	return formattime(s)

from betatest.models import *
from betatest.usersession import *
from betatest.controllers import *

def setupGlobals(sender):
	g.usersession = usersession

request_started.connect(setupGlobals)

