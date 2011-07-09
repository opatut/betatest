from betatest import *
from betatest import validators

class ChangePasswordForm(Form):
    password = PasswordField("Current password", validators=[Required(), validators.isCurrentUserPassword])
    password_new = PasswordField("New password", validators=[Required(), Length(min=6)])
    password_new2 = PasswordField("Repeat password", validators=[Required(), validators.EqualValidator("password_new")])

class ChangeTagsForm(Form):
    tag = TextField("", validators=[Required()])

class GeneralSettingsForm(Form):
    realname = TextField("Real name")
    location = TextField("Location")
    website = TextField("Website")
    email = TextField("Email", validators = [Email()])
