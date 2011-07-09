from betatest import *

@app.route("/dashboard/messages/<int:thread_id>", methods = ["GET", "POST"])
def show_message(thread_id):
    form = MessageReplyForm()
    thread = models.messagethread.MessageThread.query.filter_by(id = thread_id).first_or_404()
    usersession.loginCheck(users = thread.participants)
    user = usersession.getCurrentUser()

    if user in thread.users_unread:
        thread.users_unread.remove(user)
        db.session.commit()

    if form.validate_on_submit():
        # reply
        text = form.message.data
        m = models.message.Message(thread, text, user)
        thread.users_unread = thread.participants
        thread.markRead(user, True)
        db.session.add(m)
        db.session.commit()
        flash("Your reply has been sent.")
        return redirect(url_for("show_message", thread_id = thread.id) + "#reply-" + str(m.id))
    return render_template("dashboard-messages.html", subpage = 'messages', thread = thread, form = form)

@app.route("/dashboard/messages/new", methods = ["GET", "POST"])
@app.route("/<receiver>/contact", methods = ["GET", "POST"])
def new_message(receiver = ''):
    if not usersession.loginCheck("warning", warning_none = "Please log in to write messages."):
        return redirect(url_for("login", next = url_for("new_message", receiver = receiver)))

    form = NewMessageForm()
    c_user = usersession.getCurrentUser()

    if form.validate_on_submit():
        subject = form.subject.data
        text = form.message.data
        receivers = []
        error = False
        for name in re.split("\s*[^a-zA-Z0-9_-]+\s*", form.receiver.data):
            name = name.strip()
            if name:
                receiver = models.user.User.query.filter_by(username = name).first()
                if receiver and receiver != c_user and not receiver in receivers:
                    receivers.append(receiver)
                elif not receiver:
                    flash("The user %s cannot be found." % name, "error")
                    error = True
                    break
        if len(receivers) == 0:
            flash("You need at least one receiver.", "error")

        if not error:
            participants = receivers
            participants.append(c_user)
            thread = models.messagethread.MessageThread(subject, participants)
            message = models.message.Message(thread, text, c_user)
            db.session.add(thread)
            db.session.add(message)
            db.session.commit()
            flash("Your message has been sent.", "success")
            return redirect(message.url())

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
