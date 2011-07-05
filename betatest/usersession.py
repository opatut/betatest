from betatest import *

def login(username):
	session['logged_in'] = True
	session['username'] = username
	
def logout():
	session.pop('logged_in', None)
	session.pop('username', None)

def getCurrentUser():
	if 'username' in session:
		return models.user.User.query.filter_by(username = session['username']).first_or_404()
	else:
		return None
