from betatest import *

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    creation_date = db.Column(db.DateTime)

    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.creation_date = datetime.utcnow()

    def __repr__(self):
        return '<User %r>' % self.username

