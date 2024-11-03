from flask import abort, render_template, url_for, request, flash, session, redirect
from lecture_db import LectureDB
from werkzeug.security import generate_password_hash, check_password_hash


def user_routes(app, l_db: LectureDB):
    @app.route("/login", methods=["POST", "GET"])
    def login():
        if "userLogged" in session:
            return redirect(url_for("profile", username=session["userLogged"]))
        elif (
            request.method == "POST"
            and request.form["username"] == "root"
            and request.form["psw"] == "root"
        ):
            session["userLogged"] = request.form["username"]
            return redirect(url_for("profile", username=session["username"]))
        return render_template("login.html", title="Авторизация", menu=l_db.get_menu())

    @app.route("/register", methods=["POST", "GET"])
    def register():
        if request.method == "POST":
            session.pop("_flashes", None)
            if (
                len(request.form["name"]) > 4
                and len(request.form["email"]) > 4
                and len(request.form["psw"]) > 4
                and request.form["psw"] == request.form["psw2"]
            ):
                hash = generate_password_hash(request.form["psw"])
                res = l_db.add_user(request.form["name"], request.form["email"], hash)
                if res:
                    flash("Вы успешно зарегистрированы", "success")
                    return redirect(url_for("login"))
                else:
                    flash("Ошибка при добавлении в БД", "error")
            else:
                flash("Неверно заполнены поля", "error")

        return render_template(
            "register.html", menu=l_db.get_menu(), title="Регистрация"
        )

    @app.route("/contact", methods=["POST", "GET"])
    def contact():
        if request.method == "POST":
            if len(request.form["username"]) > 2:
                flash("Отправлено", category="success")
            else:
                flash("Имя должно быть больше 2 символов", category="error")
            print(request.form)
        return render_template("contact.html", title="Обратная связь")

    @app.route("/profile/<username>")
    def profile(username: str):
        if "userLogged" not in session or session["userLogged"] != username:
            return abort(401)
        print(username)
        return f"Пользователь: {username}"
