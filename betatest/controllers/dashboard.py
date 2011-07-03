from betatest import *

@app.route("/")
@app.route("/dashboard")
def home():
    return render_template("dashboard.html");


