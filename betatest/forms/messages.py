from betatest import *

class NewMessageForm(Form):
    subject = TextField("Subject", validators=[Required(message = "Please enter a subject"), Length(max=255)])
    receiver = TextField("Receiver", validators=[Required(message = "Please enter a receiver")])
    message = TextAreaField("Message", validators = [Required(message = "Please enter a message.")])

class MessageReplyForm(Form):
    message = TextAreaField("Message", validators = [Required(message = "Please enter a message.")])

