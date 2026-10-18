from flask import render_template, request, flash, redirect, url_for, Blueprint, session, abort
from Todo.forms import RegistrationForm, LoginForm
from Todo.models import User, List, ListItems
from Todo.extensions import bcrypt, db, login_manager
from flask_login import login_user, logout_user, current_user, login_required

main = Blueprint("main", __name__)

#---Helper functions---

@main.route("/get-list-id") # gets the new list created by the current user
@login_required
def get_list():
    if current_user.is_authenticated:
        todo_list = List(user_id=current_user.id, list_title="Untitled list")
        db.session.add(todo_list)
        db.session.commit()
        return redirect(url_for("main.create_list", list_id=todo_list.list_id))

def get_user_list_or_403(list_id):
    user_list = List.query.get(list_id) # retrieves the list
    if user_list is None: # returns a 404 error if the list is not found
        abort(404)
    if user_list.user_id != current_user.id:
        abort(403) # return a 403 error if the list doesn't belong to the logged in user
    return user_list

#---Homepage and list views---

@main.route("/")
@main.route("/home")
def home():
    if current_user.is_authenticated:
        user_lists = List.query.filter_by(user_id=current_user.id).all()
        return render_template("homepage.html", lists=user_lists, list_size=len(user_lists))
    else:
        return render_template("homepage.html")

@main.route("/create-todo/<int:list_id>")
@login_required
def create_list(list_id):
    user_list = get_user_list_or_403(list_id)
    user_list_items = ListItems.query.filter_by(list_id=list_id).all() # gets the list items
    return render_template("create_list.html", todo_list = user_list_items, list_length=len(user_list_items), list_id=list_id)

@main.route("/edit/<int:list_id>")
@login_required
def edit(list_id):
    user_list = get_user_list_or_403(list_id)
    todo_list = ListItems.query.filter_by(list_id=list_id).all()
    list_title = List.query.get(list_id).list_title
    return render_template("edit.html", list=todo_list, list_id=list_id, list_length=len(todo_list), list_title=list_title)

#---List Management---

@main.route("/save", methods=["POST"])
@login_required
def save():
    title = request.form.get("title")
    list_id = request.form.get("list_id")
    list = List.query.get(list_id)
    user_list = get_user_list_or_403(list_id)
    if not title:
        list.list_title = "Untitled list"
    else:
        list.list_title = title
    db.session.commit()
    flash("Saved", "success")
    return redirect(url_for("main.home"))

@main.route("/delete-list", methods=["POST"])
@login_required
def delete_list():
    list_id = request.form.get("list_id")
    user_list = get_user_list_or_403(list_id)
    list = List.query.get(list_id) # retrieves the list that is to be deleted
    db.session.delete(list) 
    db.session.commit()
    flash("Deleted", "danger")
    return redirect(url_for("main.home"))

#---Task Management---

@main.route("/add", methods=["POST"])
@login_required
def add():
    task = request.form.get("task", None)
    list_id = request.form.get("list_id")
    user_list = get_user_list_or_403(list_id)
    return_to = request.form.get("return_to")
    if not task:
        flash("The Task field is empty. Please add a task", "danger")
        return redirect(url_for("main.create_list", list_id=list_id))
    else:
        flash ("Task added", category="success")
        item = ListItems(list_item=task, list_id=list_id, status=False)
        db.session.add(item)
        db.session.commit() # saves the new item in database
        if return_to == "create":
            return redirect(url_for("main.create_list", list_id=list_id))
        else:
            return redirect(url_for("main.edit", list_id=list_id))

@main.route("/task-remove", methods=["POST"])
@login_required
def task_remove():
    task_id = request.form.get("task_id")
    list_id = request.form.get("list_id")
    return_to = request.form.get("return_to")
    user_list = get_user_list_or_403(list_id)
    task = ListItems.query.get(task_id) # gets the task that will be removed
    db.session.delete(task) # deletes the task from the database
    db.session.commit()
    flash("Deleted", "danger")
    if return_to == "create":
        return redirect(url_for("main.create_list", list_id=list_id))
    else:
        return redirect(url_for("main.edit", list_id=list_id))

@main.route("/task-done", methods=["POST"])
@login_required
def task_done():
    task_id = request.form.get("task_id")
    list_id = request.form.get("list_id")
    user_list = get_user_list_or_403(list_id)
    task = ListItems.query.get(task_id)
    return_to = request.form.get("return_to")
    task.status = True # marks the task as done
    db.session.add(task)
    db.session.commit()
    if return_to == "create":
        return redirect(url_for("main.create_list", list_id=list_id))
    else:
        return redirect(url_for("main.edit", list_id=list_id))

@main.route("/task-undone", methods=["POST"])
@login_required
def task_undone():
    task_id = request.form.get("task_id")
    list_id = request.form.get("list_id")
    user_list = get_user_list_or_403(list_id)
    return_to = request.form.get("return_to")
    task = ListItems.query.get(task_id)
    task.status = False # marks the task as undone
    db.session.add(task)
    db.session.commit()
    if return_to == "create":
        return redirect(url_for("main.create_list", list_id=list_id))
    else:
        return redirect(url_for("main.edit", list_id=list_id))


#---Authentication---

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

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))