from betatest import *

@app.route("/")
def home():
    if usersession.loginCheck("none"):
        return redirect(url_for("dashboard"))

    random = models.project.Project.query.order_by(db.func.random()).limit(5)
    return render_template("home.html", random = random)

@app.route("/dashboard")
@app.route("/dashboard/<page>")
def dashboard(page = 'projects'):
    if not usersession.loginCheck("warning"):
        return redirect(url_for("home"))

    user = usersession.getCurrentUser()

    if page == 'projects':
        projects = models.project.Project.query.filter_by(author_id = user.id)
        return render_template("dashboard-projects.html", subpage = page, projects = projects)
    elif page == 'tested':
        projects = models.project.Project.query.filter(models.project.Project.testers.contains(user) == True)
        return render_template("dashboard-projects.html", subpage = page, projects = projects)
    elif page == 'messages':
        return render_template("dashboard-messages.html", subpage = page, threads = user.participating_message_threads)
    elif page == 'feedback':
        projects = models.project.Project.query.all()
        return render_template("dashboard-feedback.html", subpage = page, projects = projects)
    elif page == 'notifications':
        return render_template("dashboard-notifications.html", subpage = page)

    return redirect(url_for("home"))

@app.route("/dashboard/notifications/delete/<int:id>")
def delete_notification(id):
    n = models.notification.Notification.query.filter_by(id = id).first_or_404()
    usersession.loginCheck("error", users = [n.user])
    db.session.delete(n)
    db.session.commit()
    flash("Deleted notification.", "success")
    return redirect(url_for("dashboard", page = "notifications"))

@app.route("/dashboard/notifications/delete_all")
def delete_all_notifications():
    if not usersession.loginCheck("warning"):
        return redirect(url_for("login"))
    nots = usersession.getCurrentUser().notifications
    count = len(nots.all())
    for n in nots:
        db.session.delete(n)
    db.session.commit()
    if count > 0:
        flash("Deleted all %s notifications." % count, "success")
    else:
        flash("You had no notifications to delete.", "info")
    return redirect(url_for("dashboard", page = "notifications"))
