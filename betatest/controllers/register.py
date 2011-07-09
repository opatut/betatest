from betatest import *

@app.route('/register', methods=['GET', 'POST'])
def register():
    if usersession.loginCheck("none"):
        return redirect(url_for("home"))

    form = RegisterForm()
    if form.validate_on_submit():
        user = models.user.User(form.username.data, form.password.data, form.email.data)
        db.session.add(user)
        db.session.commit()
        usersession.login(user.username)
        flash("You have been registered, %s." % user.username, "success")
        return redirect(url_for("dashboard"))


    return render_template('register.html', form = form)
