from betatest import *

@app.route("/about/")
@app.route("/help/")
@app.route("/help/<page>")
def help(page = 'about'):
	return "about: " + page
