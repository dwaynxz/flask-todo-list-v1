from Todo import app
from Todo.main import todo, ListManager, TodoList
from flask import render_template, request, flash, redirect, url_for

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

@app.route("/add-existing/<int:id_>", methods=["POST"])
def add_existing(id_):
    task = request.form.get("task")
    if not task:
        flash("The Task field is empty. Please add a task", "danger")
        return redirect(url_for("edit", id_=id_))
    else:
        current_id = to_do_lists.get_key_by_id(id_)
        current_list = to_do_lists.lists[current_id]
        current_list.add(task)
        flash ("Task added", category="success")
        return redirect(url_for("edit", id_=id_))

@app.route("/save", methods=["POST"])
def save():
    title = request.form.get("title")
    if not title:
        flash("Title cant be empty!", "danger")
        return redirect("/create-todo")
    else:
        to_do_list_copy = TodoList(to_do_list.list.copy())
        to_do_lists.add_list(title=title,todolist=to_do_list_copy)
        to_do_list.clear_list()
        flash("Saved", "success")
        return redirect("/home")

@app.route("/save-existing", methods=["POST"])
def save_existing():
    flash("Saved", "success")
    return redirect("/home")

@app.route("/edit/<int:id_>")
def edit(id_):
    current_id = to_do_lists.get_key_by_id(id_)
    current_list = to_do_lists.lists[current_id]
    return render_template("edit.html", list=current_list, id_=id_)