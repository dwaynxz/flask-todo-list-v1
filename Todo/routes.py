from Todo import app
from flask import render_template

@app.route("/")
@app.route("home")
@app.route("todo-list")
def home():
    return render_template("homepage.html")