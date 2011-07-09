from betatest import *

class RegisterForm(Form):
    username = TextField("Username", validators=[Required(), Length(max=80), validators.UsernameExists() ])
    password = PasswordField("Password", validators=[Required(), Length(min=6)])
    password_check = PasswordField("Password validation", validators=[Required(), EqualTo("password")])
    email = TextField("Email", validators=[Email(), Required()])

