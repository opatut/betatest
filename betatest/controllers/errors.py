from betatest import *

@app.errorhandler(404)
def error404(error):
	return render_template("errorpage.html", error = error, error_code = 404)
