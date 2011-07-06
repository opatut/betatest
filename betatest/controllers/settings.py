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
	usersession.loginCheck()
	
	tag_form = ChangeTagsForm()
	g_form = GeneralSettingsForm()
	pw_form = ChangePasswordForm()
	
	if request.method == "POST" and subpage == "general":
		if g_form.validate():
			user.realname = g_form.realname.data
			user.location = g_form.location.data
			user.website = g_form.website.data
			user.email = g_form.email.data
			db.session.commit()
			flash("Your changes have been saved.", "success")
		return redirect("settings")
	
	if request.method == "POST" and subpage == "password":
		if pw_form.validate():
			user.password = sha512(pw_form.password_new.data).hexdigest()
			db.session.commit()
			flash("Set new password.", "success")
		else:
			flash("Could not change password. See form below for details.", "error")
		return redirect("settings")
		
	if request.method == "POST" and subpage == "tags" and tag_form.validate():
		for tag in re.split("\s*,\s*", tag_form.tag.data):
			t = models.tag.Tag.getTag(tag.strip())
			if not t in user.tags:
				user.tags.append(t)
		db.session.commit()
		flash("Added all tags.", "success")
		return redirect("settings")
		
	return render_template("settings.html", user = usersession.getCurrentUser(), pw_form = pw_form, tag_form = tag_form, g_form = g_form)


@app.route("/settings/tags/remove/<tag>")
def settings_tags_remove(tag):
	if not usersession.loginCheck("warning"):
		return redirect(url_for("home"))
            
	models.tag.Tag.getTag(tag).users.remove(user)
	db.session.commit()
	flash("Removed tag successfully.")
	return redirect(url_for("settings"))
