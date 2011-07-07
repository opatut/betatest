from betatest import *

def userlist_check(form, field):
    error = ""
    for user in re.split("[^\w\d]*", field.data):
        if not models.user.User.query.filter_by(username = user).first():
            error += "The user " + user + " does not exist. "
    if error:
        raise ValidationError(error)

class NewMessageForm(Form):
    subject = TextField("Subject", validators=[Required(message = "Please enter a subject"), Length(max=255)])
    receiver = TextField("Receiver", validators=[Required(message = "Please enter a receiver"), userlist_check])
    message = TextAreaField("Message", validators = [Required(message = "Please enter a message.")])

class MessageReplyForm(Form):
    message = TextAreaField("Message", validators = [Required(message = "Please enter a message.")])

@app.route("/dashboard/messages/<int:message_id>", methods = ["GET", "POST"])
def show_message(message_id):
    form = MessageReplyForm()
    msg = models.message.Message.query.filter_by(id = message_id).first_or_404()
    usersession.loginCheck(users = [msg.receiver, msg.sender])
    user = usersession.getCurrentUser()
    if user == msg.receiver:
        msg.markRead(True)
    if form.validate_on_submit():
        text = form.message.data
        m = models.message.Message(msg, text, user, (msg.sender if msg.receiver == user else msg.receiver))
        db.session.add(m)
        db.session.commit()
        flash("Your message has been sent.")
        return redirect(url_for("show_message", message_id = message_id) + "#reply-" + str(m.id))
    return render_template("dashboard-messages.html", subpage = 'messages', message = msg, form = form)

@app.route("/dashboard/messages/new", methods = ["GET", "POST"])
@app.route("/<receiver>/contact", methods = ["GET", "POST"])
def new_message(receiver = ''):
    if not usersession.loginCheck("warning", warning_none = "Please log in to write messages."):
        return redirect(url_for("login", next = url_for("new_message", receiver = receiver)))

    form = NewMessageForm()
    if form.validate_on_submit():
        subject = form.subject.data
        receiver = form.receiver.data
        text = form.message.data
        r = models.user.User.query.filter_by(username = receiver).first_or_404()
        m = models.message.Message(subject, text, usersession.getCurrentUser(), r)
        db.session.add(m)
        db.session.commit()
        flash("Your message has been sent.")
        return redirect(m.url())

    return render_template("dashboard-messages.html", subpage = 'messages', newmessage = True, form = form, receiver = receiver)

@app.route("/dashboard/messages/action", methods=['GET', 'POST'])
def message_action():
    usersession.loginCheck()

    mark_unread = mark_read = False
    count = 0
    if request.form:
        mark_read = "markread" in request.form
        mark_unread = "markunread" in request.form
        delete = "delete" in request.form

        for key in request.form:
            if re.search("message-", key):
                key = key.replace("message-", "")
                msg = models.message.Message.query.filter_by(id = key).first_or_404()

                if delete:
                    return "Delete"
                elif mark_read and msg.receiver == usersession.getCurrentUser() and not msg.isread:
                    count += 1
                    msg.markRead(True)
                elif mark_unread and msg.receiver == usersession.getCurrentUser() and msg.isread:
                    count += 1
                    msg.markRead(False)

    s = ""
    if mark_read:
        s = "marked read"
    elif mark_unread:
        s = "marked unread"
    elif delete:
        s = "deleted"

    flash(str(count) + " message" + ("s" if count != 1 else "") + " have been " + s + ".", "info")
    return redirect('/dashboard/messages')
