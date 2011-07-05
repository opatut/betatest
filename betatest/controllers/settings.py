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
    password = PasswordField("Current password", validators=[Required(), isCurrentUserPassword])
    password_new = PasswordField("New password", validators=[Required(), Length(min=6)])
    password_new2 = PasswordField("Repeat password", validators=[Required(), EqualValidator("password_new")])

class ChangeTagsForm(Form):
	tag = TextField("", validators=[Required()])
	
class GeneralSettingsForm(Form):
	realname = TextField("Real name")
	location = TextField("Location")
	website = TextField("Website")
	email = TextField("Email", validators = [Email()])

@app.route("/settings", methods=['GET', 'POST'])
@app.route("/settings/<subpage>", methods=['GET', 'POST'])
def settings(subpage = ''):
	tag_form = ChangeTagsForm()
	g_form = GeneralSettingsForm()
	pw_form = ChangePasswordForm()
	if request.method == "POST" and subpage == "general":
		if g_form.validate():
			user = usersession.getCurrentUser()
			user.realname = g_form.realname.data
			user.location = g_form.location.data
			user.website = g_form.website.data
			user.email = g_form.email.data
			db.session.commit()
			flash("Your changes have been saved.", "success")
	
	if request.method == "POST" and subpage == "password":
		if pw_form.validate():
			usersession.getCurrentUser().password = sha512(pw_form.password_new.data).hexdigest()
			db.session.commit()
			flash("Set new password.", "success")
		else:
			flash("Could not change password. See form below for details.", "error")
		
	if request.method == "POST" and subpage == "tags" and tag_form.validate():
		flash("TODO: Add tag " + tag_form.tag.data, "warning")
		
		
	return render_template("settings.html", user = usersession.getCurrentUser(), pw_form = pw_form, tag_form = tag_form, g_form = g_form)
