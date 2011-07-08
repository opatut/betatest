from betatest import *
from betatest import usersession

class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship('Project', backref='bugs')
    is_closed = db.Column(db.Boolean)
    type = db.Column(db.Enum(
        'verified',
        'fixed',
        'rejected',
        'unknown'
    ))
    text = db.Column(db.Text)
    subject = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref = 'bugs')
    date = db.Column(db.DateTime)
    replies = db.relationship('BugReply', backref='bug')

    def __init__(self, text, subject, project):
        self.text = text
        self.subject = subject
        self.project = project
        self.date = datetime.utcnow()
        self.is_closed = False
        self.type = "unknown"
        self.user = usersession.getCurrentUser()
        
    def url(self):
        return url_for('project_bugtracker_bug', project = self.project.slug, username = self.project.author.username, id = self.id)
        
    def delete(self):
        for reply in self.replies:
            reply.delete()
        db.session.delete(self)
        db.session.commit()
        
