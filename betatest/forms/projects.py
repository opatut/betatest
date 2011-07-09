from betatest import *
from betatest import validators

class NewProjectForm(Form):
    title = TextField('Project title', validators = [Length(min = 6), Required(), validators.UnusedProjectSlug()])

class ProjectEditForm(Form):
    title = TextField('Project title', validators = [Length(min = 6), Required(), validators.UnusedProjectSlug()])
    homepage = TextField('Homepage', validators = [Length(min = 6)])
    description = TextAreaField('Description')

    def setProject(self, ignore_project):
        for v in self.title.validators:
            if type(v) == validators.UnusedProjectSlug:
                v.ignore_project = ignore_project

class ChangeTagsForm(Form):
    tag = TextField("", validators=[Required()])

class ProjectQuitForm(Form):
    pass

class ProjectKickForm(Form):
    pass

class ProjectApplicationForm(Form):
    text = TextAreaField("Your application letter", validators=[Required(message = "You need to write the application yourself :-P")])

class ProjectReportForm(Form):
    subject = TextField("Subject:", validators=[Required()])
    report = TextAreaField("Your Report", validators=[Required()])

class ProjectDeleteForm(Form):
    password = PasswordField("Password verification", validators=[validators.is_user_password])

class ProjectBugtrackerReportForm(Form):
    text = TextAreaField("", validators=[Required()])
    subject = TextField("Subject:", validators=[Required()])

class ProjectBugtrackerBugReplyForm(Form):
    text = TextAreaField("", validators=[Required()])

class ChangeIconForm(Form):
    icon = FileField("New Icon", validators = [Regexp('^[^/\\\\]+\\.(jpg|png|jpeg|gif)$')])
    delete = BooleanField("Delete current icon", default = False)
