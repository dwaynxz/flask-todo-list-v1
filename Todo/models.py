from Todo.extensions import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(300), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    # one user can have multiple lists
    list = db.relationship("List", backref="user", lazy=True)

class List(db.Model):
    list_id = db.Column(db.Integer, primary_key = True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    list_title = db.Column(db.String(600), nullable=False)
    # one list can have multiple list items
    list_items = db.relationship("ListItems", backref="list", lazy=True)

class ListItems(db.Model):
    list_items_id = db.Column(db.Integer, primary_key = True, unique=True)
    list_id = db.Column(db.Integer, db.ForeignKey("list.list_id"))
    list_item = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))