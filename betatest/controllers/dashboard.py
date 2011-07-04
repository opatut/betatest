from betatest import *


@app.route("/")
@app.route("/dashboard")
@app.route("/dashboard/<page>")
def dashboard(page = 'projects'):
	user = usersession.getCurrentUser()
	if user == None:
		return render_template("home.html")
	
	if page == 'projects':
		projects = models.project.Project.query.filter_by(author_id = user.id)
		return render_template("dashboard-projects.html", subpage = page, projects = projects)
	elif page == 'tested':
		projects = models.project.Project.query.filter(models.project.Project.testers.contains(user) == True)
		return render_template("dashboard-projects.html", subpage = page, projects = projects)
	elif page == 'messages':
		messages = models.message.Message.query.filter_by(receiver_id = user.id)
		return render_template("dashboard-messages.html", subpage = page, messages = messages)
	elif page == 'feedback':
		projects = models.project.Project.query.all()
		return render_template("dashboard-projects.html", subpage = page, projects = projects)
	
	return redirect(url_for("home"))

@app.route("/dashboard/messages/<int:message_id>")
def show_message(message_id):
	user = usersession.getCurrentUser()
	if user != None:
		msg = models.message.Message.query.filter_by(id = message_id).first_or_404()
		return render_template("dashboard-messages.html", subpage = 'messages', message = msg)
	
	return redirect(url_for("home"))
	
def userlist_check(field):
	error = ""
	for user in re.split("[^\w\d]*", field.data):
		if not models.user.User.query.filter_by(username = user).first():
			error.append(user+" does not exist.\n")
	if error:
		raise ValidationError(error)
	
class NewMessageForm(Form):
	subject = TextField("Subject", validators=[Required(), Length(max=255)])
	receiver = TextField("Receiver", validators=[Required(), userlist_check])
	message = TextAreaField("Message")

@app.route("/dashboard/messages/new")
def new_message():
	user = usersession.getCurrentUser()
	if user == None:
		return render_template("home.html")
	
	form = NewMessageForm()
	if form.validate_on_submit():
		subject = form.subject.data
		receiver = form.receiver.data
		message = form.receiver.data
	
	return render_template("dashboard-messages.html", subpage = 'messages', newmessage=True, form = form)
