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
		projects = models.project.Project.query.all()
		return render_template("dashboard-projects.html", subpage = page, projects = projects)
	elif page == 'messages':
		messages = models.message.Message.query.filter_by(receiver_id = user.id)
		return render_template("dashboard-messages.html", subpage = page, messages = messages)
	elif page == 'feedback':
		projects = models.project.Project.query.all()
		return render_template("dashboard-projects.html", subpage = page, projects = projects)
	
	return redirect(url_for("home"))

@app.route("/dashboard/messages/<int:msg_id>")
def messages(msg_id):
	user = usersession.getCurrentUser()
	if user == None:
		return render_template("home.html")
	
	if msg_id >= 0:
		msg = models.message.Message.query.filter_by(id = msg_id).first()
		return render_template("dashboard-messages.html", subpage = 'messages', message = msg)
	
	return redirect(url_for("home"))
