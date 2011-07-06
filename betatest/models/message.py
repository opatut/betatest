from betatest import *

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    message = db.Column(db.Text)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    send_date = db.Column(db.DateTime)
    isread = db.Column(db.Boolean)
    reply_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    reply = db.relationship('Message', backref = db.backref('parent', uselist = False), remote_side = 'Message.id')

    def __init__(self, title_or_parent, message, sender, receiver):
        if isinstance(title_or_parent, str):
            self.title = title_or_parent
        else:
            # parent
            self.parent = title_or_parent.getFollowingThread()[-1]
            self.title = self.parent.title
        self.message = message
        self.send_date = datetime.utcnow()
        self.isread = False
        self.sender = sender
        self.receiver = receiver

    def __repr__(self):
        return '<Message: %r>' % self.title

    def getThreadRootMessage(self):
        if self.isThreadRoot():
            return self
        else:
            return self.parent.getThreadRootMessage()

    def getCompleteThread(self):
        if self.isThreadRoot():
            return self.getFollowingThread()
        else:
            return self.getThreadRootMessage().getFollowingThread()

    def getFollowingThread(self):
        if not self.reply:
            return [self]
        else:
            thread = self.reply.getFollowingThread()
            thread.insert(0, self)
            return thread

    def isThreadRoot(self):
        return not self.parent

    def markRead(self, read = True):
        for msg in self.getCompleteThread():
            msg.isread = read
        db.session.commit()
