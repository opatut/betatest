from betatest import *

@app.route("/")
def home():
    if usersession.loginCheck("none"):
        return redirect(url_for("dashboard"))
    return render_template("home.html")

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
        messages = models.message.Message.query.filter(db.and_(
                db.or_(models.message.Message.receiver_id == user.id,
                        models.message.Message.sender_id == user.id),
                models.message.Message.reply == None)).order_by(models.message.Message.send_date.desc())
        return render_template("dashboard-messages.html", subpage = page, messages = messages)
    elif page == 'feedback':
        projects = models.project.Project.query.all()
        return render_template("dashboard-feedback.html", subpage = page, projects = projects)
    elif page == 'notifications':
        return render_template("dashboard-notifications.html", subpage = page)

    return redirect(url_for("home"))

@app.route("/dashboard/notifications/delete/<int:id>")
def delete_notification(id):
    flash("Todo: delete notification", "warning")
    return redirect(url_for("home"))

@app.route("/dashboard/notifications/delete_all")
def delete_all_notifications():
    flash("Todo: delete all notifications", "warning")
    return redirect(url_for("home"))
