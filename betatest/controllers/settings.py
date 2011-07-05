from betatest import *

def isCurrentUserPassword(form, field):
	if sha512(field.data).hexdigest() != usersession.getCurrentUser().password:
		raise ValidationError("Thats not your password.")

class EqualValidator(object):
	def __init__(self, other):
		self.other = other
	
	def __call__(self, form, field):
		if field.data != form[self.other].data:
			raise ValidationError("Values do not match.")

class ChangePasswordForm(Form):
    password = PasswordField("current Password", validators=[Required(), isCurrentUserPassword])
    password_new = PasswordField("new Password", validators=[Required(), Length(min=6)])
    password_new2 = PasswordField("retype new Password", validators=[Required(), EqualValidator("password_new")])

class ChangeTagsForm(Form):
	tag = TextField("", validators=[Required()])

@app.route("/settings", methods=['GET', 'POST'])
def settings():
	tag_form = ChangeTagsForm()
		
	pw_form = ChangePasswordForm()
	if pw_form.validate_on_submit():
		usersession.getCurrentUser().password = sha512(pw_form.password_new.data).hexdigest()
		db.session.commit()
		flash("Set new password.", "success")
	return render_template("settings.html", user = usersession.getCurrentUser(), pw_form = pw_form, tag_form = tag_form)
