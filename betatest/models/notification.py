from betatest import *
from betatest.models.application import Application


'''
Notification module. Nofications can have the following types:

* Notification.ApplicationStatus(status, project)

All notification types that have a project linked support the getProject() method.
'''

class Data(object):
    notification = None

    def getProject(self):
        if self.project_id:
            return models.project.Project.query.filter_by(id = self.project_id).first()
        else:
            return None

    def _render(self):
        return "Generic notification."

class ApplicationStatus(Data):
    ''' status can be one of the following:
        * accepted
        * declined
        * created
    '''
    status = ""
    application_id = 0

    def __init__(self, status, application):
        self.status = status.lower()
        db.session.commit() # commit or the id might not be set
        self.application_id = application.id

    def getApplication(self):
        if not self.application_id:
            abort_reason(500, "A notification contains invalid data: %s" % self.application_id)
        return Application.query.filter_by(id = self.application_id).first()

    def getProject(self):
        return getApplication().project

    def _render(self):
        a = self.getApplication()
        if self.status in ["created", "accepted", "declined"]:
            return render_template("notifications/application_" + self.status + ".html",
                application = a,
                notification = self.notification)
        else:
            abort_reason(500, "Invalid status (%s) for ApplicationStatus in Notification." % self.status) # internal server error


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    object = db.Column(db.PickleType())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, user, object):
        self.user = user
        self.object = object

    def render(self):
        self.object.notification = self
        return self.object._render()

    def __repr__(self):
        return "<Notification {0}:{1}>".format(self.user.username, self.id)

    def delete(self):
        db.session.delete(self)
