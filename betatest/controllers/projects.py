from betatest import *
import os, sys
from werkzeug import secure_filename

def is_allowed_filename(filename, extensions = ["png", "jpg", "jpeg", "gif"]):
    return '.' in filename and filename.lower().rsplit('.', 1)[1] in extensions

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
    # to find the XX projects with the most testers
    # - join the project_testers table
    # - group_by Project.id
    # - within order_by use func.count to count testers
    # - limit the result size

    # SELECT * FROM project JOIN project_testers ON project_testers.project_id = project.id GROUP BY project.id  ORDER BY count(project.id) DESC LIMIT 10;
    projects = models.project.Project.query.join(models.project.project_testers).group_by(models.project.Project.id).order_by(db.desc(db.func.count(models.project.project_testers.c.tester_id))).limit(10)
    return render_template("projects-list.html", subpage = tab, delete_tag_endpoint = 'project_tags_remove', projects = projects)


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

@app.route("/<username>/<project>/testers/kick/")
def project_kicklist(username, project):
    u = models.user.User.query.filter_by(username = username).first_or_404()
    p = models.project.Project.query.filter_by(slug = project.lower(), author_id = u.id).first_or_404()
    usersession.loginCheck(users = [u])
    return render_template("project-kicklist.html", user = u, project = p)

@app.route("/<username>/<project>/testers/kick/<tester>", methods = ["POST", "GET"])
def project_kick_tester(username, project, tester):
    u = models.user.User.query.filter_by(username = username).first_or_404()
    p = models.project.Project.query.filter_by(slug = project.lower(), author_id = u.id).first_or_404()
    usersession.loginCheck(users = [u])
    t = models.user.User.query.filter_by(username = tester).first_or_404()

    if not t in p.testers:
        flash("%s is not tester of this project." % t.username, "error")
        return redirect(p.url())

    form = ProjectKickForm()
    if form.validate_on_submit():
        p.testers.remove(t)
        db.session.add(models.notification.Notification(t, models.notification.ProjectQuit(p, t, True)))
        db.session.commit()
        flash("You have kicked %s from the project." % t.username, "success")
        return redirect(p.url())

    return render_template("project-kick.html", username = username, project = p, tester = t, form = form)


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
    elif request.method != "POST":
        form.title.data = p.title
        form.description.data = p.description
        form.homepage.data = p.homepage

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

@app.route("/<username>/<project>/changeicon", methods = ["POST", "GET"])
def project_change_icon(username, project):
    u = models.user.User.query.filter_by(username = username).first_or_404()
    usersession.loginCheck(users = [u])
    p = models.project.Project.query.filter_by(slug = project.lower(), author_id = u.id).first_or_404()

    form = ChangeIconForm()

    if form.validate_on_submit():
        file = request.files[form.icon.name]
        if file and is_allowed_filename(file.filename):
            name = str(p.id) + "." + file.filename.lower().rsplit('.', 1)[1]
            name = secure_filename(name)
            p.iconfile = name
            file.save(p.getIconFile())
            db.session.commit()
            flash("Your icon has been changed.", "success")
        elif form.delete.data:
            return "Gotta delete the icon."

    return render_template("project-change-icon.html", form = form, project = p)

@app.route("/<username>/<project>/icon")
@app.route("/<username>/<project>/icon/<size>")
def project_icon(username, project, size = 32):
    u = models.user.User.query.filter_by(username = username).first_or_404()
    p = models.project.Project.query.filter_by(slug = project.lower(), author_id = u.id).first_or_404()

    if p.iconfile:
        # todo: scale and cache
        return send_file(p.getIconFile())
    else:
        abort(404)


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

@app.route("/<username>/<project>/quit", methods = ["POST", "GET"])
def project_quit(username, project):
    u = models.user.User.query.filter_by(username = username).first_or_404()
    p = models.project.Project.query.filter_by(slug = project.lower(), author_id = u.id).first_or_404()

    if not usersession.loginCheck("none", users = p.testers):
        flash("You have to be tester to quit this project.", "warning")
        return redirect(p.url())

    form = ProjectQuitForm()
    if form.validate_on_submit():
        c_user = usersession.getCurrentUser()
        p.testers.remove(c_user)
        db.session.add(models.notification.Notification(p.author, models.notification.ProjectQuit(p, c_user)))
        db.session.commit()
        flash("You have quit the project.", "success")
        return redirect(p.url())

    return render_template("project-quit.html", username = username, project = p, form = form)


