from flask import Flask, render_template, url_for, request, flash

app = Flask(__name__)
app.config["SECRET_KEY"] = "fASbA_A12312_asdS"
menu = [
    {"name": "Установка", "url": "install-flask"},
    {"name": "Первое приложение", "url": "first-app"},
    {"name": "Обратная связь", "url": "contact"},
]


@app.route("/hellow")
def hello():
    print(url_for("hello"))
    return "<h1>Hellow</h1>"


@app.route("/")
def index():
    return render_template("index.html", title="Про Flask", menu=menu)

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
    print(username)
    return ""


if __name__ == "__main__":
    app.run(debug=True)
