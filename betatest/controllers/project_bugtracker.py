from betatest import *

@app.route("/<username>/<project>/delete", methods = ["POST"])
def delete_project(username, project):
    u = models.user.User.query.filter_by(username = username).first_or_404()
    p = models.project.Project.query.filter_by(slug = project.lower(), author_id = u.id).first_or_404()

    usersession.loginCheck(users = [u])

    form = forms.ProjectDeleteForm()
    if form.validate_on_submit():
        p.delete()
        db.session.commit()
        flash("Too sad... your project has been deleted completely. It's gone now. Forever. :(", "success")
        return redirect(url_for("dashboard"))
    else:
        flash("Your project has NOT been deleted. Your request failed.", "error")
        return redirect(url_for("project_edit", username = username, project = project))
    
@app.route("/<username>/<project>/bugtracker")
def project_bugtracker(username, project):
    u = models.user.User.query.filter_by(username = username).first_or_404()
    p = models.project.Project.query.filter_by(slug = project.lower(), author_id = u.id).first_or_404()
    users = [p.testers]
    users.append(u)
    usersession.loginCheck(users)
    
    return render_template("project-bugtracker.html", project = p)

@app.route("/<username>/<project>/bugtracker/report", methods=["GET", "POST"])
def project_bugtracker_report(username, project):
    u = models.user.User.query.filter_by(username = username).first_or_404()
    p = models.project.Project.query.filter_by(slug = project.lower(), author_id = u.id).first_or_404()
    users = [p.testers]
    users.append(u)
    usersession.loginCheck(users)
    
    form = forms.ProjectBugtrackerReportForm()
    
    if form.validate_on_submit():
        b = models.bug.Bug(form.text.data, form.subject.data, p)
        db.session.add(b)
        db.session.commit()
        return redirect(b.url())
    
    return render_template("project-bugtracker-report.html", project = p, form = form)

@app.route("/<username>/<project>/bugtracker/<int:id>", methods=["GET", "POST"])
def project_bugtracker_bug(username, project, id):
    u = models.user.User.query.filter_by(username = username).first_or_404()
    p = models.project.Project.query.filter_by(slug = project.lower(), author_id = u.id).first_or_404()
    users = [p.testers]
    users.append(u)
    usersession.loginCheck(users)
    
    b = models.bug.Bug.query.filter_by(project_id = p.id, id = id).first_or_404()
    form = forms.ProjectBugtrackerBugReplyForm()
    
    if form.validate_on_submit():
        r = models.bugreply.BugReply(form.text.data, b)
        db.session.commit()
        return redirect(b.url())
    
    return render_template("project-bugtracker-bug.html", project = p, bug = b, form = form)
