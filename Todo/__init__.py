from flask import Flask
from dotenv import load_dotenv
import os
from Todo.extensions import db, bcrypt, login_manager

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = "login"
    from Todo.routes import main
    app.register_blueprint(main)
    return app