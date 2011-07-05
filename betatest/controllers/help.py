from betatest import *

@app.route("/about/")
@app.route("/help/")
@app.route("/help/<path:page>")
def help(page = 'about'):
	return "about: " + page
