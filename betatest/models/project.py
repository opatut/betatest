from betatest import *

project_testers = db.Table('project_testers', db.Model.metadata,
    db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
    db.Column('tester_id', db.Integer, db.ForeignKey('user.id'))
)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creation_date = db.Column(db.DateTime)
    testers = db.relationship("User", secondary = project_testers, backref = "tested_projects")    

    def __init__(self, title, description, author):
        self.title = title
        self.description = description
        self.creation_date = datetime.utcnow()
        self.author = author

    def __repr__(self):
		return '<Project: %r>' % self.title
