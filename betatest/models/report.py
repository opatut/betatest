from betatest import *

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(256))
    report = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    
    def __init__(self, report, project_id):
        self.report = report
        self.project_id = project_id
