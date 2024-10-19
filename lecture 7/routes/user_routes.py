from flask import abort, render_template, url_for, request, flash, session, redirect


def user_routes(app, menu):
    @app.route('/login', methods=["POST", "GET"])
    def login():
        if "userLogged" in session:
            return redirect(url_for('profile', username=session['userLogged']))
        elif request.method == "POST" and request.form['username'] == "root" and request.form['psw'] == "root":
            session['userLogged'] = request.form['username']
            return redirect(url_for('profile', username=session['username']))
        return render_template("login.html", title="Авторизация", menu=menu)
    
    @app.route("/contact", methods=["POST", "GET"])
    def contact():
        if request.method == "POST":
            if len(request.form["username"]) > 2:
                flash("Отправлено", category="success")
            else:
                flash("Имя должно быть больше 2 символов", category="error")
            print(request.form)
        return render_template("contact.html", title="Обратная связь", menu=menu)

    @app.route("/profile/<username>")
    def profile(username: str):
        if 'userLogged' not in session or session['userLogged'] != username:
            return abort(401)
        print(username)
        return f"Пользователь: {username}"
