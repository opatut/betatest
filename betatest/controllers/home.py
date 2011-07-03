from betatest import app

@app.route("/")
def home():
    return "Hello World in view."

