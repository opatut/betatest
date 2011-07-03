

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    pa = db.Column(db.String(128))
    email = db.Column(db.String(256), unique=True)
    registered = db.Column(db.DateTime)
    verified = db.Column(db.Boolean)
    entries = db.relationship('Entry', backref='participant', lazy='dynamic')

    def __init__(self, username, password, email):
        self.username = username
        self.password = sha512(password).hexdigest()
        self.email = email
        self.registered = datetime.utcnow()
        self.verified = False

    def __repr__(self):
        return '<User %r>' % self.username

