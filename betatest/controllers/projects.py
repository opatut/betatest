from betatest import *

@app.route("/projects/new", methods = ["POST", "GET"])
def new_project():
    if not usersession.loginCheck("warning", warning_none = "Please log in to create a project."):
        return redirect(url_for("login", next = url_for("new_project")))

    form = NewProjectForm()
    if form.validate_on_submit():
        user = usersession.getCurrentUser()
        project = models.project.Project(form.title.data, "", user)
        db.session.add(project)
        db.session.commit()
        flash("Your project has been created. You can now edit its details.", "success")
        return redirect(url_for("project_edit", username = user.username, project = project.slug))

    return render_template("projects-new.html", subpage = "new", form = form)

@app.route("/projects")
@app.route("/projects/<tab>")
def projects(tab = "list"):
    return render_template("projects.html", subpage = tab, delete_tag_endpoint = 'project_tags_remove')


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

@app.route("/<username>/<project>/edit", methods=['GET', 'POST'])
@app.route("/<username>/<project>/edit/<subpage>", methods = ["GET", "POST"])
def project_edit(username, project, subpage = ''):
    u = models.user.User.query.filter_by(username = username).first_or_404()

    usersession.loginCheck(users = [u])

    p = models.project.Project.query.filter_by(slug = project.lower(), author_id = u.id).first_or_404()

    tag_form = ChangeTagsForm()
    delete_form = ProjectDeleteForm()
    form = ProjectEditForm()
    form.setProject(p)

    if subpage == "general" and form.validate_on_submit():
        p.title = form.title.data
        p.slug = models.project.titleToSlug(form.title.data)
        p.homepage = form.homepage.data
        p.description = form.description.data
        db.session.commit()
        flash("Your changes have been applied.", "success")
        return redirect(p.url())
    else:
        form.description.data = p.description

    if subpage == "tags" and tag_form.validate_on_submit():
        for tag in re.split("\s*,\s*", tag_form.tag.data):
            t = models.tag.Tag.getTag(tag.strip())
            if not t in p.tags:
                p.tags.append(t)
        db.session.commit()
        flash("Added all tags.", "success")

    return render_template("project-edit.html",
        user = u,
        project = p,
        form = form,
        tag_form = tag_form,
        delete_form = delete_form,
        tags = p.tags)

@app.route("/<username>/<project>/tags/remove/<tag>")
def project_tags_remove(username, project, tag):
    u = models.user.User.query.filter_by(username = username).first_or_404()

    usersession.loginCheck(users = [u])

    p = models.project.Project.query.filter_by(slug = project.lower(), author_id = u.id).first_or_404()
    if usersession.getCurrentUser().id == p.author_id:
        models.tag.Tag.getTag(tag).projects.remove(p)
        db.session.commit()
        flash("Removed tag successfully.")
        return redirect(url_for("project_edit", username = username, project = project))
    else:
        abort_reason(403, "You are not the author of this project.")
