from betatest import *

@app.route("/search")
def search():
	q = request.args.get('q', '')
	if q:
		projects = models.project.Project.query.filter(db.or_(
			models.project.Project.description.like("%"+q+"%"),
			models.project.Project.title.like("%"+q+"%"),
			models.project.Project.homepage.like("%"+q+"%")
			)).all()
		users = models.user.User.query.filter(db.or_(
			models.user.User.username.like("%"+q+"%"),
			models.user.User.realname.like("%"+q+"%"),
			models.user.User.website.like("%"+q+"%")
			)).all()
			
		if len(projects) == 1 and len(users) == 0:
			# only 1 project, redirect there
			return redirect(projects[0].url())
		if len(projects) == 0 and len(users) == 1:
			# only 1 user, redirect there
			return redirect(users[0].url())
			
		return render_template("search.html", queried = True, users = users, projects = projects)
	else:
		return render_template("search.html", queried = False)
