from betatest import *

'''
Notification module. Nofications can have the following types:

* Notification.ApplicationStatus(status, project)

All notification types that have a project linked support the getProject() method.
'''

class Notification(db.Model):
    class Data(object):
        def getProject(self):
            if self.project_id:
                return models.project.Project.query.filter_by(id = self.project_id).first()
            else:
                return None

    class ApplicationStatus(Data):
        ''' status can be one of the following:
            * accepted
            * declined
            * created
        '''
        def __init__(self, status, project):
            self.project_id = project.id
            self.status = status

    id = db.Column(db.Integer, primary_key=True)
    object = db.Column(db.PickleType())
    text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, user, text, object):
        self.user = user
        self.text = text
        self.object = object

