from flask import Flask
from routes.routers import register_routes
import os
from db import create_db
from flask_login import LoginManager
from admin.admin import admin


DATABASE = "./db.db"
SECRET_KEY = "fASbA_A12312_asdS"
DEBUG = True
MAX_CONTENT_LENGTH = 10000 * 10000


def create_app():
    app = Flask(__name__)
    app.register_blueprint(admin, url_prefix="/admin")
    app.config.from_object(__name__)
    app.config.update(dict(DATABASE=os.path.join(app.root_path, "ada.db")))
    login_manager = LoginManager(app)
    create_db(app)
    register_routes(app, login_manager)

    return app
