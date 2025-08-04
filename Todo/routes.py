from Todo import app
from Todo.main import todo, Lists
from flask import render_template, request, flash, redirect

to_do_list = todo
to_do_lists = Lists()

@app.route("/")
@app.route("/home")
def home():
    return render_template("homepage.html", to_do_list=to_do_list)

@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task", None)
    if not task:
        flash("The Task field is empty. Please add a task", "danger")
        return redirect("/")
    else:
        todo.add(task)
        flash ("Task added", category="success")
        return redirect("/")

@app.route("/save", methods=["POST"])
def save():
    title = request.form.get("title")
    if not title:
        flash("Title cant be empty!", "danger")
        return redirect("/home")
    else:
        to_do_lists.add_list(title=title,todolist=to_do_list)
        todo.new_list()
        flash("Saved", "success")
        return redirect("/home")