from flask import Flask, session, redirect, url_for, escape, request, \
        render_template

from flaskext.sqlalchemy import SQLAlchemy
from flaskext.wtf import *
from datetime import datetime, timedelta
from hashlib import sha512
	
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///betatest.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'aio3ujhrsdflncm239mlehasudkj<bkm'
db = SQLAlchemy(app)

#define filters

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
	return s.strftime("%Y-%m-%d %H:%M:%S")

from betatest.models import *
from betatest.usersession import *
from betatest.controllers import *
