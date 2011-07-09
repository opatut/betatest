from betatest import *

class MessageThreadReadMark(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    thread = db.relationship("MessageThread", backref = db.backref("read_marks"))
    thread_id = db.Column(db.Integer, db.ForeignKey("message_thread.id"))
    user = db.relationship("User", backref = db.backref("messagethread_read_marks", uselist = False))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    read_date = db.Column(db.DateTime)

    def __init__(self, user, thread):
        self.thread = thread
        self.user = user
        self.update()

    def update(self):
        self.read_date = datetime.utcnow()

    def delete(self):
        db.session.delete(self)
