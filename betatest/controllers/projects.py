from betatest import *

@app.route("/projects/new")
def new_project():
	return render_template("projects-new.html", subpage = "new")

@app.route("/projects")
@app.route("/projects/interesting")
def projects():
	return render_template("projects.html", subpage = "interesting")


@app.route("/<username>/<project>")
def project(username, project):
	user = models.user.User.query.filter_by(username = username).first_or_404()
	project = models.project.Project.query.filter_by(slug = project.lower(), author_id = user.id).first_or_404()
	
	return render_template("project.html", user = user, project = project)

@app.route("/<username>/<project>/testers")
def project_testers(username, project):	
	user = models.user.User.query.filter_by(username = username).first_or_404()
	project = models.project.Project.query.filter_by(slug = project.lower(), author_id = user.id).first_or_404()
	
	return render_template("project.html", user = user, project = project, testers = True)
