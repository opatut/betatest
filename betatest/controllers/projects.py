from betatest import *

class UnusedProjectSlug(object):
    def __init__(self, ignore_project = None):
        self.ignore_project = ignore_project

    def __call__(self, form, field):
        user = usersession.getCurrentUser()
        new_slug = models.project.titleToSlug(field.data)
        project = user.findProject(new_slug)
        # we have a project with that name
        if project and (self.ignore_project == None or self.ignore_project != project):
            raise ValidationError("You already have a project with a similar title. Please choose another one.")


class NewProjectForm(Form):
    title = TextField('Project title', validators = [Length(min = 6), Required(), UnusedProjectSlug()])

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

class ProjectEditForm(Form):
    title = TextField('Project title', validators = [Length(min = 6), Required(), UnusedProjectSlug()])
    homepage = TextField('Homepage', validators = [Length(min = 6)])
    description = TextAreaField('Description')

    def setProject(self, ignore_project):
        for v in self.title.validators:
            if type(v) == UnusedProjectSlug:
                v.ignore_project = ignore_project

class ChangeTagsForm(Form):
    tag = TextField("", validators=[Required()])

@app.route("/<username>/<project>/edit", methods=['GET', 'POST'])
@app.route("/<username>/<project>/edit/<subpage>", methods = ["GET", "POST"])
def project_edit(username, project, subpage = ''):
    u = models.user.User.query.filter_by(username = username).first_or_404()

    usersession.loginCheck(users = [u])

    p = models.project.Project.query.filter_by(slug = project.lower(), author_id = u.id).first_or_404()

    tag_form = ChangeTagsForm()
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

    return render_template("project-edit.html", user = u, project = p, form = form, tag_form = tag_form, tags = p.tags)

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

class ProjectApplicationForm(Form):
    text = TextAreaField("Your application letter", validators=[Required(message = "You need to write the application yourself :-P")])

@app.route("/<username>/<project>/apply", methods=["GET", "POST"])
def project_apply(username, project):
    if not usersession.loginCheck("warning"):
        return redirect(url_for('login', next = url_for('project_apply', username = username, project = project)))

    form = ProjectApplicationForm()
    user = usersession.getCurrentUser()
    u = models.user.User.query.filter_by(username = username).first_or_404()
    p = models.project.Project.query.filter_by(slug = project.lower(), author_id = u.id).first_or_404()

    a = models.application.Application.query.filter_by(user_id = user.id, project_id = p.id).first()

    if a:
        if a.status == 'unread':
            flash("You allready have applied for this project.", "error")
            return redirect(p.url())
        elif a.status == 'accepted':
            flash("You are allready tester of this project.", "error")
            return redirect(p.url())

    if form.validate_on_submit():
        if user.username == u.username:
            flash("You can't apply to your own project.", "error")
            return redirect(p.url())
        a = models.application.Application(p, form.text.data)
        a.user = user
        db.session.commit()
        flash("Sent application succesfully", "success")
        return redirect(p.url())
    return render_template("project-apply.html", form = form, project = p)

@app.route("/<username>/<project>/applications")
def project_applications(username, project, applicant = None):
    u = models.user.User.query.filter_by(username = username).first_or_404()
    usersession.loginCheck(users = [u])
    p = models.project.Project.query.filter_by(slug = project.lower(), author_id = u.id).first_or_404()
    return render_template("project-applications.html", project = p)


@app.route("/<username>/<project>/applications/<applicant>")
def project_application_details(username, project, applicant):
        u = models.user.User.query.filter_by(username = username).first_or_404()
        usersession.loginCheck(users = [u])
        p = models.project.Project.query.filter_by(slug = project.lower(), author_id = u.id).first_or_404()
        application_sender = models.user.User.query.filter_by(username = applicant).first_or_404()
        a = models.application.Application.query.filter_by(project_id = p.id, user_id = application_sender.id).first_or_404()
        return render_template("project-application-details.html", project = p, application = a)

class ProjectReportForm(Form):
    subject = TextField("Subject:", validators=[Required()])
    report = TextAreaField("Your Report", validators=[Required()])

@app.route("/<username>/<project>/report", methods=["GET", "POST"])
def project_report(username, project):
    u = models.user.User.query.filter_by(username = username).first_or_404()
    p = models.project.Project.query.filter_by(slug = project.lower(), author_id = u.id).first_or_404()
    users = [p.testers]
    users.append(u)
    usersession.loginCheck(users)
    form = ProjectReportForm()

    if form.validate_on_submit():
        r = models.report.Report(form.report.data, form.subject.data, p.id)
        db.session.add(r)
        db.session.commit()
        flash("Report has ben successfully submited.", "success")
        return redirect(url_for('project_reports', username = username, project = project))

    return render_template("project-report.html", project = p, form = form)

@app.route("/<username>/<project>/reports")
def project_reports(username, project):
    u = models.user.User.query.filter_by(username = username).first_or_404()
    p = models.project.Project.query.filter_by(slug = project.lower(), author_id = u.id).first_or_404()
    users = [p.testers]
    users.append(u)
    usersession.loginCheck(users)

    return render_template("project-reports.html", project = p)

@app.route("/<username>/<project>/report/<int:id>")
def project_report_details(username, project, id):
    u = models.user.User.query.filter_by(username = username).first_or_404()
    p = models.project.Project.query.filter_by(slug = project.lower(), author_id = u.id).first_or_404()
    users = [p.testers]
    users.append(u)
    usersession.loginCheck(users)
    r = models.report.Report.query.filter_by(project_id = p.id, id = id).first_or_404()

    return render_template("project-report-details.html", project = p, report = r)
