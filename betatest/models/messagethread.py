from betatest import *
import random

message_thread_users_unread = db.Table('message_thread_users_unread', db.Model.metadata,
    db.Column('thread_id', db.Integer, db.ForeignKey('message_thread.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

message_thread_participants = db.Table('message_thread_participants', db.Model.metadata,
    db.Column('thread_id', db.Integer, db.ForeignKey('message_thread.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class MessageThread(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    subject = db.Column(db.String(256))
    messages = db.relationship("Message", backref = db.backref("thread", uselist = False))
    users_unread =  db.relationship('User',
        secondary = message_thread_users_unread,
        backref = "unread_message_threads",
        primaryjoin = 'MessageThread.id == message_thread_users_unread.c.thread_id',
        secondaryjoin = 'User.id == message_thread_users_unread.c.user_id')
    participants =  db.relationship('User',
        secondary = message_thread_participants,
        backref = "participating_message_threads",
        primaryjoin = 'MessageThread.id == message_thread_participants.c.thread_id',
        secondaryjoin = 'User.id == message_thread_participants.c.user_id')

    def __init__(self, subject, participants):
        self.subject = subject
        self.participants = participants

    def markRead(self, user, read = True):
        if read and user in self.users_unread:
            self.users_unread.remove(user)
        elif not read and not user in self.user_unread:
            self.users_unread.add(user)
        db.session.commit()

    def __repr__(self):
        return '<MessageThread: %r>' % self.id

    def delete(self):
        for message in self.messages:
            message.delete()
        db.session.delete(self)


    def getRandomParticipants(self, limit = 0, exclude = None):
        r = self.participants
        random.shuffle(r)
        x = []
        count = 0
        for p in r:
            if p != exclude:
                count += 1
                x.append(p)
                if limit != 0 and count >= limit:
                    break
        return x
