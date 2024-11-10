from flask import abort, render_template, url_for, request, flash, session, redirect, make_response
from lecture_db import LectureDB
from werkzeug.security import generate_password_hash, check_password_hash
from auth.auth_user import UserLogin
from flask_login import login_user, login_required, current_user
from forms.forms import LoginForm


def user_routes(app, l_db: LectureDB):
    @app.route("/login", methods=["POST", "GET"])
    def login():
        
        if current_user.is_authenticated:
            return redirect(url_for('profile'))
 
        form = LoginForm()
        if form.validate_on_submit():
            user = l_db.get_user_by_email(form.email.data)
            if user and check_password_hash(user['psw'], form.psw.data):
                userlogin = UserLogin().create(user)
                rm = form.remember.data
                login_user(userlogin, remember=rm)
                return redirect(request.args.get("next") or url_for("profile"))
    
            flash("Неверная пара логин/пароль", "error")
    
        return render_template("login.html", menu=l_db.get_menu(), title="Авторизация", form=form)
    
    

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

    @app.route("/profile")
    @login_required
    def profile():
        return render_template("profile.html", menu=l_db.get_menu(), title="Профиль")
    
    @app.route('/userava')
    @login_required
    def userava():
        img = current_user.getAvatar(app)
        if not img:
            return ""
    
        h = make_response(img)
        h.headers['Content-Type'] = 'image/png'
        return h
    
    @app.route('/upload', methods=["POST", "GET"])
    @login_required
    def upload():
        if request.method == 'POST':
            file = request.files['file']
            if file and current_user.verifyExt(file.filename):
                try:
                    img = file.read()
                    res = l_db.updateUserAvatar(img, current_user.get_id())
                    if not res:
                        flash("Ошибка обновления аватара", "error")
                        return redirect(url_for('profile'))
                    flash("Аватар обновлен", "success")
                except FileNotFoundError as e:
                    flash("Ошибка чтения файла", "error")
            else:
                flash("Ошибка обновления аватара", "error")
    
        return redirect(url_for('profile'))
