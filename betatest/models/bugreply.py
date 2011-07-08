from betatest import *
from betatest import usersession

class BugReply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bug_id = db.Column(db.Integer, db.ForeignKey('bug.id'))
    date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref = 'bugreplies')
    text = db.Column(db.Text)
    
    def __init__(self, text, bug):
        self.text = text
        self.bug = bug
        self.user = usersession.getCurrentUser()
        self.date = datetime.utcnow()
    
    def delete(self):
        db.session.delete(self)
