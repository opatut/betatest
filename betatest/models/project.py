# -*- coding: latin-1 -*-

from betatest import *
import re

project_testers = db.Table('project_testers', db.Model.metadata,
    db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
    db.Column('tester_id', db.Integer, db.ForeignKey('user.id'))
)

def titleToSlug(s):
	s = s.lower()
	s = s.replace("ä","ae")
	s = s.replace("ö","oe")
	s = s.replace("ü","ue")
	s = s.replace("ß","ss")
	s = re.sub(r"[\s_+]+", "-", s)
	s = re.sub("[^a-z0-9\-]", "", s)
	return s
	
	

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    slug = db.Column(db.String(80))
    description = db.Column(db.Text)
    homepage = db.Column(db.String(128))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creation_date = db.Column(db.DateTime)
    testers = db.relationship("User", secondary = project_testers, backref = "tested_projects")    

    def __init__(self, title, description, author, homepage = ''):
        self.title = title
        self.generateSlug()
        self.description = description
        self.creation_date = datetime.utcnow()
        self.author = author
        self.homepage = homepage
        
    def url(self):
		return url_for("project", username = self.author.username, project = self.slug)
        
    def generateSlug(self):
		self.slug = titleToSlug(self.title)
		return self.slug

    def __repr__(self):
		return '<Project: %r>' % self.title
