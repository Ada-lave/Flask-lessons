from flask import abort, render_template, request, flash
from db import get_db
from lecture_db import LectureDB
from flask_login import login_required

def post_routes(app, l_db: LectureDB):

    @app.route("/add_post", methods=["POST", "GET"])
    def add_post():
        if request.method == "POST":
            if len(request.form["name"]) > 4 and len(request.form["post"]) > 10:
                res = l_db.add_post(
                    request.form["name"], request.form["post"], request.form["url"]
                )

                if not res:
                    flash("Ошибка добавления статьи", category="error")
                else:
                    flash("Успешно добавленно", category="success")
            else:
                flash("Ошибка добавления статьи", category="error")

        return render_template(
            "add_post.html", menu=l_db.get_menu(), title="Добавление статьи"
        )

    @app.route("/posts/<alias>")
    @login_required
    def show_post(alias: str):
        title, post = l_db.get_post(alias)

        if not title:
            abort(404)

        return render_template(
            "show_post.html", menu=l_db.get_menu(), title=title, post=post
        )
