from betatest import *

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(256), unique=True)
    registered_date = db.Column(db.DateTime)
    projects = db.relationship('Project', backref='author', lazy='dynamic')
    outbox = db.relationship('Message', backref='sender', lazy='dynamic', primaryjoin='Message.sender_id == User.id')
    inbox = db.relationship('Message', backref='receiver', lazy='dynamic', primaryjoin='Message.receiver_id == User.id')

    def __init__(self, username, password, email):
        self.username = username
        self.password = sha512(password).hexdigest()
        self.email = email
        self.registered_date = datetime.utcnow()

    def __repr__(self):
        return '<User: %r>' % self.username
        
    def getNewMessageCount(self): 
		i = 0
		for msg in self.inbox:
			if not msg.isread:
				i += 1
		return i
