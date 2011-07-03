from betatest import *

class LoginForm(Form):
    username = TextField("Username", validators=[Required(), Length(max=80)])
    password = PasswordField("Password", validators=[Required()])

@app.route('/login', methods=['GET', 'POST'])
def login():    
	error = None
	form = LoginForm()
	if form.validate_on_submit():
		username = form.username.data
		password = sha512(form.password.data).hexdigest()
		user = models.user.User.query.filter_by(username = username).first()
		if not user:
			error = 'Invalid username.'
		elif not user.password == password:
			error = 'Invalid password.'
		else:
			usersession.login(username)
			return render_template('home.html', message = 'Welcome back, %s.' % username);
	return render_template('login.html', form = form, error = error)


@app.route('/logout')
def logout():
	usersession.logout()
	return render_template("home.html", message = "You have been logged out.");
