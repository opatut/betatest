from betatest import *

@app.route("/dashboard/messages/<int:message_id>")
def show_message(message_id):
    msg = models.message.Message.query.filter_by(id = message_id).first_or_404()
    usersession.loginCheck(users = [msg.receiver, msg.sender])
    if user == msg.receiver:
        msg.markRead(True)
    return render_template("dashboard-messages.html", subpage = 'messages', message = msg)

def userlist_check(field):
	error = ""
	for user in re.split("[^\w\d]*", field.data):
		if not models.user.User.query.filter_by(username = user).first():
			error.append(user+" does not exist.\n")
	if error:
		raise ValidationError(error)
	
class NewMessageForm(Form):
	subject = TextField("Subject", validators=[Required(), Length(max=255)])
	receiver = TextField("To", validators=[Required(), userlist_check])
	message = TextAreaField("Message")

@app.route("/dashboard/messages/new")
@app.route("/<receiver>/contact")
def new_message(receiver = ''):
	if not usersession.loginCheck("warning", warning_none = "Please log in to write messages."):
		return redirect(url_for("login", next = url_for("new_message", receiver = receiver)))
	
	form = NewMessageForm()
	if form.validate_on_submit():
		subject = form.subject.data
		receiver = form.receiver.data
		message = form.receiver.data
	
	return render_template("dashboard-messages.html", subpage = 'messages', newmessage=True, form = form, receiver = receiver)

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
				elif mark_read and msg.receiver == usersession.getCurrentUser():
					count += 1
					msg.markRead(True)
				elif mark_unread and msg.receiver == usersession.getCurrentUser():
					count += 1
					msg.markRead(False)
					
	if mark_read:
		flash(str(count) + " messages have been marked read.", "info")
	if mark_unread:
		flash(str(count) + " messages have been marked unread.", "info")
	if delete:
		flash(str(count) + " messages have been deleted.", "info")
	return redirect('/dashboard/messages')
