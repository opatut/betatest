from betatest import *
import os, sys, jinja2

@app.route("/help")
@app.route("/help/<path:page>")
def help(page = 'index'):
    try:
        return render_template("help/" + page + ".html")
    except jinja2.exceptions.TemplateNotFound:
        abort_reason(404, "Invalid help page.")
