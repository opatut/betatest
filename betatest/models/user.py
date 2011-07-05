from betatest import *
from betatest.models.project import Project
import re

def isBlockedUsername(u):
	u = u.lower()
	if re.search("[^a-zA-Z0-9]", u):
		return False
	if u in ["admin", "about", "help", "contact", "privacy", "settings", "user", "project", "dashboard", "login", "logout"]:
		return False
	if len(u) < 6:
		return False
	return True

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    realname = db.Column(db.String(128))
    location = db.Column(db.String(128))
    website = db.Column(db.String(128))
    password = db.Column(db.String(128))
    email = db.Column(db.String(256), unique=True)
    registered_date = db.Column(db.DateTime)
    projects = db.relationship('Project', backref='author', lazy='dynamic')
    outbox = db.relationship('Message', backref='sender', lazy='dynamic', primaryjoin='Message.sender_id == User.id')
    inbox = db.relationship('Message', backref='receiver', lazy='dynamic', primaryjoin='Message.receiver_id == User.id')

    def __init__(self, username, password, email, realname = '', location = '', website = ''):
        self.username = username
        self.password = sha512(password).hexdigest()
        self.email = email
        self.registered_date = datetime.utcnow()
        self.realname = realname
        self.location = location
        self.website = website

    def url(self):
        return url_for("profile", username = self.username)

    def __repr__(self):
        return '<User: %r>' % self.username
        
    def getNewMessageCount(self): 
        i = 0
        for msg in self.inbox:
            if not msg.isread and msg.reply == None:
                i += 1
        return i

    def getAvatar(self, size = 32):
        return "http://www.gravatar.com/avatar/{0}?s={1}&d=identicon".format(md5(self.email.lower()).hexdigest(), size)
        
    def findProject(self, slug):
		return Project.query.filter_by(slug = slug.lower(), author_id = self.id).first()

