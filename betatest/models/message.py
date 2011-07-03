from betatest import *

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    message = db.Column(db.Text)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    send_date = db.Column(db.DateTime)
    isread = db.Column(db.Boolean)

    def __init__(self, title, message, sender, receiver):
        self.title = title
        self.message = message
        self.send_date = datetime.utcnow()
        self.isread = False
        self.sender = sender
        self.receiver = receiver

    def __repr__(self):
        return '<Message: %r>' % self.title

