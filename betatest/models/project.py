from betatest import *

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creation_date = db.Column(db.DateTime)

    def __init__(self, title, description, author):
        self.title = title
        self.description = description
        self.creation_date = datetime.utcnow() - timedelta(days = 10)
        self.author = author

    def __repr__(self):
		return '<Project: %r>' % self.title
