from Todo import app
from Todo.main import todo, ListManager
from flask import render_template, request, flash, redirect

to_do_list = todo
to_do_lists = ListManager()

@app.route("/")
@app.route("/home")
def home():
    return render_template("homepage.html", to_do_lists=to_do_lists)

@app.route("/create-todo")
def create_list():
    return render_template("create_list.html", to_do_list=to_do_list)

@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task", None)
    if not task:
        flash("The Task field is empty. Please add a task", "danger")
        return redirect("/create-todo")
    else:
        todo.add(task)
        flash ("Task added", category="success")
        return redirect("/create-todo")

@app.route("/save", methods=["POST"])
def save():
    title = request.form.get("title")
    if not title:
        flash("Title cant be empty!", "danger")
        return redirect("/create-todo")
    else:
        to_do_lists.add_list(title=title,todolist=to_do_list)
        todo.new_list()
        flash("Saved", "success")
        return redirect("/home")