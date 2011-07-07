from betatest import *

@app.route("/search")
def search(tag = None):
    q = request.args.get('q', '')
    f = request.args.get('f', '')

    if q or tag != None:
        projects = []
        users = []
        if f != "f" or request.args.get('p',''):
            projects = models.project.Project.query.filter(db.or_(
                models.project.Project.description.like("%"+q+"%"),
                models.project.Project.title.like("%"+q+"%"),
                models.project.Project.homepage.like("%"+q+"%")
                )).all()
        if f != "f" or request.args.get('u',''):
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

        return render_template("search.html", source = "query", users = users, projects = projects)
    else:
        return render_template("search.html")

@app.route("/tags")
@app.route("/tags/<tag>")
def tags(tag = ""):
    if not tag:
        flash("Todo: tags list", "info")
        return render_template("search.html")
    else:
        t = models.tag.Tag.getTag(tag, False)
        if not t:
            flash("The tag %s cannot be found.".format(tag), "info")
            return redirect("tags")
        projects = models.project.Project.query.filter(models.project.Project.tags.contains(t)).all()
        users = models.user.User.query.filter(models.user.User.tags.contains(t)).all()
        return render_template("search.html", source = "tag", tag = t, users = users, projects = projects)
