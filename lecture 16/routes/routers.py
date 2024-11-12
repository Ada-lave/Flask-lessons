from flask import (
    render_template,
    url_for,
    make_response,
    url_for,
    redirect,
    Flask,
    request,
)
from .user_routes import user_routes
from .post_routes import post_routes
from lecture_db import LectureDB
from flask_login import LoginManager
from auth.auth_user import UserLogin


def register_routes(app: Flask, login_manager: LoginManager):
    l_db = LectureDB(app.config["DATABASE"])
    user_routes(app, l_db)
    post_routes(app, l_db)

    @app.errorhandler(404)
    def page_not_found(error):
        return ("Page not found", 404)
    
    @login_manager.user_loader
    def load_user(user_id: int):
        print(f"load_user: {user_id}")
        user = l_db.get_user(user_id)
        return UserLogin().fromDB(user)

    @app.route("/redirect")
    def red():
        return redirect(url_for("index"), 301)

    @app.route("/")
    def index():
        content = render_template(
            "index.html",
            title="Про Flask",
            menu=l_db.get_menu(),
            posts=l_db.get_posts(),
        )
        res = make_response(content)

        return res

    @app.route("/cookie")
    def cookie():
        log = ""
        if request.cookies.get("logged"):
            log = request.cookies.get("logged")

        res = make_response(f"<h1>Авторизован</h1> logged: {log}")
        res.set_cookie("logged", "yes")

        return res

    @app.route("/cookie_del")
    def cookie_del():
        res = make_response(f"<h1>Куки удален</h1>")
        res.set_cookie("logged", "", 0)

        return res
