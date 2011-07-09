from betatest import *

@app.route("/<username>/<project>/report", methods=["GET", "POST"])
def project_report(username, project):
    u = models.user.User.query.filter_by(username = username).first_or_404()
    p = models.project.Project.query.filter_by(slug = project.lower(), author_id = u.id).first_or_404()
    users = [p.testers]
    users.append(u)
    usersession.loginCheck(users)
    form = forms.ProjectReportForm()

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
