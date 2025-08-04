from Todo import app
from Todo.main import todo
from flask import render_template, request, flash, redirect

to_do_list = todo

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