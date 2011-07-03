from betatest import *

@app.route("/")
@app.route("/dashboard")
@app.route("/dashboard/<page>")
def home(page = 'projects'):
	user = usersession.getCurrentUser()
	user = models.user.User.query.filter_by(username = "opatut").first()
	if user == None:
		return render_template("home.html")
	
	if page == 'projects':
		projects = models.project.Project.query.filter_by(author_id = user.id)
		return render_template("dashboard-projects.html", subpage = page, projects = projects)
	elif page == 'tested':
		projects = models.project.Project.query.all()
		return render_template("dashboard-projects.html", subpage = page, projects = projects)
	elif page == 'messages':
		projects = models.project.Project.query.all()
		return render_template("dashboard-projects.html", subpage = page, projects = projects)
	elif page == 'feedback':
		projects = models.project.Project.query.all()
		return render_template("dashboard-projects.html", subpage = page, projects = projects)
	else:
		return ""
