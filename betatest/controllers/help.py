from betatest import *
import os, sys

about_pages = {
    "about"     : "About",
    "contact"     : "Contact",
    "terms-of-service" : "Terms of Service",
    "privacy"    : "Privacy",
}

@app.route("/help")
@app.route("/help/<path:page>")
def help(page = 'index'):
    if page in about_pages:
        filename = sys.path[0] + "/betatest/pages/" + page + ".md"
        if not os.path.isfile(filename):
            abort_reason(404, "Help page not found.")
        md = file.read(open(filename , "r"))
        return render_template("static.html", title = about_pages[page], content = md)
    else:
        abort_reason(404, "Invalid help page.")
