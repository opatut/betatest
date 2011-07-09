from betatest import *
from betatest.models.messagethreadreadmark import MessageThreadReadMark
import random

message_thread_participants = db.Table('message_thread_participants', db.Model.metadata,
    db.Column('thread_id', db.Integer, db.ForeignKey('message_thread.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class MessageThread(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    subject = db.Column(db.String(256))
    messages = db.relationship("Message", backref = db.backref("thread", uselist = False))
    participants =  db.relationship('User',
        secondary = message_thread_participants,
        backref = "participating_message_threads",
        primaryjoin = 'MessageThread.id == message_thread_participants.c.thread_id',
        secondaryjoin = 'User.id == message_thread_participants.c.user_id')

    def __init__(self, subject, participants):
        self.subject = subject
        self.participants = participants

    def __repr__(self):
        return '<MessageThread: %r>' % self.id

    def delete(self):
        for message in self.messages:
            message.delete()
        db.session.delete(self)


    def getRandomParticipants(self, limit = 0, exclude = None):
        r = list(self.participants) # make a copy to shuffle!
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

    def getUserReadDate(self, user = None):
        if user == None:
            user = usersession.getCurrentUser()
        for mark in self.read_marks:
            if mark.user == user:
                return mark.read_date
        return None

    def isReadByUser(self, user = None):
        # true if the last message was sent before the last read date
        readdate = self.getUserReadDate(user)
        return readdate and self.messages[-1].send_date < readdate

    def markAsRead(self, read = True, user = None):
        if user == None:
            user = usersession.getCurrentUser()

        if not read: # mark as unread
            for mark in self.read_marks:
                if mark.user == user:
                    mark.delete()
        else: # mark as read
            done = False
            for mark in self.read_marks:
                if mark.user == user:
                    mark.update()
                    done = True
            # we had no read mark yet, create one
            if not done:
                db.session.add(MessageThreadReadMark(user, self))

        db.session.commit()

    def deleteForUser(self, user = None):
        if user == None:
            user = usersession.getCurrentUser()
        self.participants.remove(user)
        db.session.commit()
        if not self.participants:
            self.delete()
            db.session.commit()
