from Todo import app
from Todo.main import todo
from flask import render_template, request

to_do_list = todo

@app.route("/")
@app.route("home")
@app.route("/todo-list")
def home():
    return render_template("homepage.html", to_do_list=to_do_list)

@app.route("/add", methods="POST")
def add():
    pass