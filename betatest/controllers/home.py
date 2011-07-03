from betatest import *

@app.route("/test")
def home():
    return render_template("home.html");

