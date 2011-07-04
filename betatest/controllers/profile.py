from betatest import *

@app.route("/<username>")
def profile(username):
	user = models.user.User.query.filter_by(username = username).first_or_404()
	
	return render_template("profile.html", user = user)
