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
	u = models.user.User.query.filter_by(username = username).first_or_404()
	p = models.project.Project.query.filter_by(slug = project.lower(), author_id = u.id).first_or_404()
	return render_template("project-details.html", user = u, project = p)

@app.route("/<username>/<project>/testers")
def project_testers(username, project):	
	u = models.user.User.query.filter_by(username = username).first_or_404()
	p = models.project.Project.query.filter_by(slug = project.lower(), author_id = u.id).first_or_404()
	return render_template("project-details.html", user = u, project = p, testers = True)
	
class ProjectEditForm(Form):
	title = TextField('Project title', validators = [Length(min = 6), Required()])
	homepage = TextField('Homepage', validators = [Length(min = 6)])
	description = TextAreaField('Description')
	#public = CheckboxInput('Public visible')
	
@app.route("/<username>/<project>/edit", methods = ["GET", "POST"])
def project_edit(username, project):
	u = models.user.User.query.filter_by(username = username).first_or_404()
	if u != usersession.getCurrentUser():
		abort(403)
	else:
		form = ProjectEditForm()
		p = models.project.Project.query.filter_by(slug = project.lower(), author_id = u.id).first_or_404()
		
		if form.validate_on_submit():
			new_slug = models.project.titleToSlug(form.title.data)
			if new_slug != p.slug and u.findProject(new_slug):
				flash("You already have a project with a similar title. Please choose another one.", "error")
			else:
				p.title = form.title.data
				p.slug = new_slug
				p.homepage = form.homepage.data
				p.description = form.description.data
				db.session.commit()
				flash("Your changes have been applied.", "success")
				return redirect(p.url())
		else:	
			form.description.data = p.description
		return render_template("project-edit.html", user = u, project = p, form = form)
