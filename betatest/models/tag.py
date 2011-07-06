from betatest import *

project_tags = db.Table('project_tags', db.Model.metadata,
    db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.UniqueConstraint('project_id', 'tag_id')
)

user_tags = db.Table('user_tags', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.UniqueConstraint('user_id', 'tag_id')
)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64))
    projects  = db.relationship('Project', backref='tags', lazy='dynamic', secondary = project_tags)
    users = db.relationship('User', backref='tags', lazy='dynamic', secondary = user_tags)

    def __init__(self, tag):
        self.tag = tag.lower()

    def url(self):
        return url_for("tags", tag = self.tag)

    def __repr__(self):
        return '<Tag: %r>' % self.tag

    @classmethod
    def getTag(self, tag, create = True):
        first = Tag.query.filter_by(tag = tag.lower()).first()
        if first:
            return first
        elif create:
            # make a new tag
            t = Tag(tag)
            db.session.add(t)
            db.session.commit()
            return t
        else:
            return None
