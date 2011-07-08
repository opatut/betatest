# -*- coding: utf-8 -*-

from betatest import *

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    creation_date = db.Column(db.DateTime)
    text = db.Column(db.Text)
    status = db.Column(db.Enum(
        'declined',
        'accepted',
        'read',
        'unread'
    ))

    def __init__(self, project, text):
        self.project = project
        self.text = text
        self.creation_date = datetime.utcnow()
        self.status = 'unread'

    def __repr__(self):
        return "<Application %r>" % self.id

    def url(self):
        return url_for('project_application_details',
            username = self.project.author.username,
            project = self.project.slug,
            applicant = self.user.username)

    def delete(self):
        db.session.delete(self)
