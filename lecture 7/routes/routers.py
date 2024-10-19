from flask import render_template, url_for, request, flash
from .user_routes import user_routes
from .post_routes import post_routes
from db import get_db
from lecture_db import LectureDB

menu = [
    {"name": "Установка", "url": "install-flask"},
    {"name": "Первое приложение", "url": "first-app"},
    {"name": "Обратная связь", "url": "contact"},
]


def register_routes(app):
    user_routes(app, menu)
    post_routes(app)

    @app.errorhandler(404)
    def page_not_found(error):
        db = get_db(app)
        l_db = LectureDB(db)
        return render_template("page404.html", menu=l_db.get_menu(), title="Ошибка")

    @app.route("/hellow")
    def hello():
        print(url_for("hello"))
        return "<h1>Hellow</h1>"

    @app.route("/")
    def index():
        db = get_db(app)
        l_db = LectureDB(db)
        return render_template("index.html", title="Про Flask", menu=l_db.get_menu(), posts=l_db.get_posts())
