from betatest import *

@app.route("/ajax/add_project_tag/<int:project_id>/<tag>")
def ajax_add_project_tag(project_id, tag):
    project = models.project.Project.query.filter_by(id = project_id).first()
    for tag in re.split("\s*,\s*", tag):
        t = models.tag.Tag.getTag(tag.strip())
        if not t in project.tags:
            project.tags.append(t)
    db.session.commit()
    return render_template("tags_list.html", tags = project.tags, delete_tag_endpoint = 'ajax_project_tags_remove')

@app.route("/ajax/add_user_tag/<tag>")
def ajax_add_user_tag(tag):
    user = usersession.getCurrentUser()
    for tag in re.split("\s*,\s*", tag):
        t = models.tag.Tag.getTag(tag.strip())
        if not t in user.tags:
            user.tags.append(t)
    db.session.commit()
    return render_template("tags_list.html", tags = user.tags, delete_tag_endpoint = 'ajax_settings_tags_remove')


@app.route("/ajax/remove_project_tag/<int:project_id>/<tag>")
def ajax_remove_project_tag(project_id, tag):
    project = models.project.Project.query.filter_by(id = project_id).first()
    t = models.tag.Tag.getTag(tag.strip())
    if t in project.tags:
        t.projects.remove(project)
        db.session.commit()
    return render_template("tags_list.html", tags = project.tags, delete_tag_endpoint = 'ajax_project_tags_remove')

@app.route("/ajax/remove_user_tag/<tag>")
def ajax_remove_user_tag(tag):
    user = usersession.getCurrentUser()
    t = models.tag.Tag.getTag(tag.strip())
    if t in user.tags:
        t.users.remove(user)
        db.session.commit()
    return render_template("tags_list.html", tags = user.tags, delete_tag_endpoint = 'ajax_settings_tags_remove')
