from betatest import *

@app.route('/login', methods=['GET', 'POST'])
def login(next = ""):
    if request.method != "POST" and usersession.loginCheck("none"):
        return redirect(next)

    if next:
        session["next"] = next

    error = None
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = sha512(form.password.data).hexdigest()
        user = models.user.User.query.filter_by(username = username).first()
        if not user:
            error = 'That username is wrong.'
        elif not user.password == password:
            error = 'That\'s not your password.'
        else:
            usersession.login(username)
            flash("Welcome back, %s." % username, "success")
            if "next" in session:
                n = redirect(session["next"])
                session.pop("next")
                return redirect(n)
            else:
                return redirect(url_for("dashboard"))

    return render_template('login.html', form = form, error = error)


@app.route('/logout')
def logout():
    usersession.logout()
    flash("You have been logged out.")
    return redirect(url_for("home"))
