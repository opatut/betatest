from betatest import *

def userlist_check(form, field):
    error = ""
    for user in re.split("[^\w\d]*", field.data):
        if not models.user.User.query.filter_by(username = user).first():
            error += "The user " + user + " does not exist. "
    if error:
        raise ValidationError(error)
def is_user_password(form, field):
    hash = sha512(field.data).hexdigest()
    if hash != usersession.getCurrentUser().password:
        raise ValidationError("That is not your password.")
        
def isCurrentUserPassword(form, field):
    if sha512(field.data).hexdigest() != usersession.getCurrentUser().password:
        raise ValidationError("Thats not your password.")

class EqualValidator(object):
    def __init__(self, other):
        self.other = other

    def __call__(self, form, field):
        if field.data != form[self.other].data:
            raise ValidationError("Values do not match.")

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
