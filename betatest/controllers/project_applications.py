from betatest import *

@app.route("/<username>/<project>/apply", methods=["GET", "POST"])
def project_apply(username, project):
    if not usersession.loginCheck("warning"):
        return redirect(url_for('login', next = url_for('project_apply', username = username, project = project)))

    form = forms.ProjectApplicationForm()
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
