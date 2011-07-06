from betatest import *
import os, sys

about_pages = {
	"about" 	: "About",
	"contact" 	: "Contact",
	"terms-of-service" : "Terms of Service",
	"privacy"	: "Privacy",
}

@app.route("/about")
@app.route("/help")
@app.route("/help/<path:page>")
def help(page = 'about'):
	if page in about_pages:
		filename = sys.path[0] + "/betatest/pages/" + page + ".md"
		md = file.read(open(filename , "r"))
		return render_template("static.html", title = about_pages[page], content = md)
	else:
		abort(404)
