from betatest import *

@app.route("/settings")
def settings():
	return render_template("settings.html", user = usersession.getCurrentUser())
