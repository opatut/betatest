from betatest import *

@app.route("/ajax/add_project_tag/<int:project_id>/<tag>")
def ajax_add_project_tag(project_id, tag):
    project = models.project.Project.query.filter_by(id = project_id).first()
    usersession.loginCheck(user = project.author)
    for tag in re.split("\s*,\s*", tag):
        t = models.tag.Tag.getTag(tag.strip())
        if not t in project.tags and tag:
            project.tags.append(t)
    db.session.commit()
    return render_template("tags_list.html", tags = project.tags, delete_tag_endpoint = 'ajax_project_tags_remove')

@app.route("/ajax/add_user_tag/<tag>")
def ajax_add_user_tag(tag):
    usersession.loginCheck()
    user = usersession.getCurrentUser()
    for tag in re.split("\s*,\s*", tag):
        t = models.tag.Tag.getTag(tag.strip())
        if not t in user.tags and tag:
            user.tags.append(t)
    db.session.commit()
    return render_template("tags_list.html", tags = user.tags, delete_tag_endpoint = 'ajax_settings_tags_remove')


@app.route("/ajax/remove_project_tag/<int:project_id>/<tag>")
def ajax_remove_project_tag(project_id, tag):
    project = models.project.Project.query.filter_by(id = project_id).first()
    usersession.loginCheck(user = project.author)
    t = models.tag.Tag.getTag(tag.strip())
    if t in project.tags:
        t.projects.remove(project)
        db.session.commit()
    return render_template("tags_list.html", tags = project.tags, delete_tag_endpoint = 'ajax_project_tags_remove')

@app.route("/ajax/remove_user_tag/<tag>")
def ajax_remove_user_tag(tag):
    usersession.loginCheck()
    user = usersession.getCurrentUser()
    t = models.tag.Tag.getTag(tag.strip())
    if t in user.tag:
        t.users.remove(user)
        db.session.commit()
    return render_template("tags_list.html", tags = user.tags, delete_tag_endpoint = 'ajax_settings_tags_remove')


@app.route("/ajax/tags/autocomplete")
def ajax_tags_autocomplete():    
    q = request.args.get("query", "")
    if q:
        tags = models.tag.Tag.query.filter(models.tag.Tag.tag.like("%" + q + "%")).all()
        json = '{query:"' + q +'", suggestions: ['
        for tag in tags:
            json += '"' + tag.tag + '", '
        json += ']}'
        return json
    return ""
 


@app.route("/ajax/users/autocomplete")
def ajax_users_autocomplete():    
    q = request.args.get("query", "")
    if q:
        users = models.user.User.query.filter(db.or_(
            models.user.User.username.like("%" + q + "%"),
            models.user.User.realname.like("%" + q + "%"))).all()
        json = '{query:"' + q +'", suggestions: ['
        for user in users:
            r = '' if not user.realname else ('(' + user.realname + ')')
            json += '\'<div class="icon"><img width="16" height="16" src="{0}" /></div> <div class="username">{1} <span class="realname">{2}</span></div>\', '.format(user.getAvatar(16), user.username, r)
        json += '], data: ['
        for user in users:
            json += '"' + user.username + '", '
        json += ']}'
        return json
    return ""
