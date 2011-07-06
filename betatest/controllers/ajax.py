from betatest import *

@app.route("/ajax/add_project_tag/<slug>/<tag>")
def ajax_add_project_tag(slug, tag):
    project = models.project.Project.query.filter_by(slug = slug).first()
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
