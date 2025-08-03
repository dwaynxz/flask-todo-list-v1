from Todo import app
from Todo.main import todo
from flask import render_template, request

@app.route("/")
@app.route("home")
@app.route("todo-list")
def home():
    return render_template("homepage.html")

@app.route("/add", methods="POST")
def add():
    pass