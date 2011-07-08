from betatest import *

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('message_thread.id'))
    message = db.Column(db.Text)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    send_date = db.Column(db.DateTime)

    def __init__(self, thread, message, sender):
        self.thread = thread
        self.send_date = datetime.utcnow()
        self.message = message
        self.sender = sender

    def __repr__(self):
        return '<Message: %r>' % self.id

    def url(self):
         return url_for('show_message', thread_id = self.thread_id) + "#reply-" + str(self.id)

    def delete(self):
        db.session.delete(self)
