from Todo.main import todo, ListManager, TodoList
from flask import render_template, request, flash, redirect, url_for, Blueprint, session
from Todo.forms import RegistrationForm, LoginForm
from Todo.models import User, List, ListItems
from Todo.extensions import bcrypt, db, login_manager
from flask_login import login_user, logout_user, current_user

main = Blueprint("main", __name__)

to_do_list = todo
to_do_lists = ListManager()

@main.route("/")
@main.route("/home")
def home():
    # if current_user.is_authenticated:
    #     last_list = List.query.filter_by(user_id=current_user.id)[-1]
    #     if len(last_list.query.all()) == 0:
    #         db.session.delete(last_list)
    #         db.session.commit()
    return render_template("homepage.html", to_do_lists=to_do_lists)

@main.route("/get-list-id") # gets the new list created by the current user
def get_list():
    if current_user.is_authenticated:
        todo_list = List(user_id=current_user.id)
        db.session.add(todo_list)
        db.session.commit()
        return redirect(url_for("main.create_list", list_id=todo_list.list_id))

@main.route("/create-todo/<int:list_id>")
def create_list(list_id):
    user_list_items = ListItems.query.filter_by(list_id=list_id).all()
    return render_template("create_list.html", todo_list = user_list_items, list_length=len(user_list_items))

@main.route("/add", methods=["POST"])
def add():
    task = request.form.get("task", None)
    if not task:
        flash("The Task field is empty. Please add a task", "danger")
        return redirect(url_for("main.create_list"))
    else:
        todo.add(task)
        flash ("Task added", category="success")
        # if current_user.is_authenticated:

        return redirect(url_for("main.create_list"))

@main.route("/add-existing/<int:id_>", methods=["POST"])
def add_existing(id_):
    task = request.form.get("task")
    if not task:
        flash("The Task field is empty. Please add a task", "danger")
        return redirect(url_for("main.edit", id_=id_))
    else:
        current_list = to_do_lists.fetch_list(id_)
        current_list.add(task)
        flash ("Task added", category="success")
        return redirect(url_for("main.edit", id_=id_))

@main.route("/save", methods=["POST"])
def save():
    title = request.form.get("title")
    if not title:
        flash("Title cant be empty!", "danger")
        return redirect(url_for("main.create_list"))
    else:
        to_do_list_copy = TodoList(to_do_list.list.copy())
        to_do_lists.add_list(title=title,todolist=to_do_list_copy)
        to_do_list.clear_list()
        flash("Saved", "success")
        return redirect(url_for("main.home"))

@main.route("/save-existing", methods=["POST"])
def save_existing():
    flash("Saved", "success")
    return redirect(url_for("main.home"))

@main.route("/edit/<int:id_>")
def edit(id_):
    current_list = to_do_lists.fetch_list(id_)
    return render_template("edit.html", list=current_list, id_=id_)

@main.route("/delete-existing/<int:id_>", methods=["POST"])
def delete_existing(id_):
    current_key = to_do_lists.get_key_by_id(id_)
    to_do_lists.delete_list(current_key)
    flash("Deleted", "danger")
    return redirect(url_for("main.home"))

@main.route("/task-remove/<int:task_id>", methods=["POST"])
def task_remove(task_id):
    key = to_do_list.get_key_by_id(task_id)
    to_do_list.delete_task(key)
    return redirect(url_for("main.create_list"))

@main.route("/task-done/<int:task_id>", methods=["POST"])
def task_done(task_id):
    to_do_list.mark_task_done(task_id)
    return redirect(url_for("main.create_list"))

@main.route("/task-undone/<int:task_id>", methods=["POST"])
def task_undone(task_id):
    to_do_list.mark_task_undone(task_id)
    return redirect(url_for("main.create_list"))

@main.route("/existing-task-remove/<int:id_>/<int:task_id>", methods=["POST"])
def existing_task_remove(id_, task_id):
    current_list = to_do_lists.fetch_list(id_)
    key = current_list.get_key_by_id(task_id)
    current_list.delete_task(key)
    return redirect(url_for("main.edit", id_=id_))

@main.route("/existing-task-done/<int:id_>/<int:task_id>", methods=["POST"])
def existing_task_done(id_, task_id):
    current_list = to_do_lists.fetch_list(id_)
    current_list.mark_task_done(task_id)
    return redirect(url_for("main.edit", id_=id_))

@main.route("/existing-task-undone/<int:id_>/<int:task_id>", methods=["POST"])
def existing_task_undone(id_, task_id):
    current_list = to_do_lists.fetch_list(id_)
    current_list.mark_task_undone(task_id)
    return redirect(url_for("main.edit", id_=id_))


#---Registration route---
@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # retrieve data from the form
        name = form.name.data
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Account already exists. Please register or use a different email.", "danger")
        else:
            user = User(name=name, email=email, password=bcrypt.generate_password_hash(password=password))
            db.session.add(user)
            db.session.commit() # add user to the database
            flash("Account Created Sucessfully", "success")
            return redirect(url_for("main.home"))
    return render_template("register.html", form=form)

#---Login route---
@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Account doesn't exist. Please register", "danger")
            return redirect(url_for("main.home"))
        else:
            if not bcrypt.check_password_hash(user.password, password): # check password hash
                flash("Incorrect password", "danger")
            else:
                login_user(user)
                flash("Logged in successfully", "success")
                return redirect(url_for("main.home"))
    return render_template("login.html", form=form)

#---Logout route---
@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))