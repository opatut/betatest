from betatest import *
from betatest.models.user import User

def userlist_check(form, field):
    error = ""
    for user in re.split("[^\w\d]*", field.data):
        if not models.user.User.query.filter_by(username = user).first():
            error += "The user " + user + " does not exist. "
    if error:
        raise ValidationError(error)

def is_user_password(form, field):
    if sha512(field.data).hexdigest() != usersession.getCurrentUser().password:
        raise ValidationError("That is not your password.")

class UnusedProjectSlug(object):
    def __init__(self, ignore_project = None):
        self.ignore_project = ignore_project

    def __call__(self, form, field):
        user = usersession.getCurrentUser()
        new_slug = models.project.titleToSlug(field.data)
        project = user.findProject(new_slug)
        # we have a project with that name
        if project and (self.ignore_project == None or self.ignore_project != project):
            raise ValidationError("You already have a project with a similar title. Please choose another one.")

class UsernameExists(object):
    def __init__(self, message = "The username already exists."):
        self.message = message

    def __call__(self, form, field):
        if User.query.filter_by(username = field.data).first() != None:
            raise ValidationError(self.message)

class Not(object):
    def __init__(self, call, message = None):
        self.call = call
        self.message = message

    def __call__(self, form, field):
        errored = False
        try:
            self.call(form, field)
        except ValidationError:
            # there was an error, so don't do anything
            errored = True

        if not errored:
            raise ValidationError(self.call.message if self.message == None else self.message)
