from betatest import *

@app.errorhandler(403)
@app.errorhandler(404)
def errorpage(error):
    return render_template("errorpage.html", error = error)
