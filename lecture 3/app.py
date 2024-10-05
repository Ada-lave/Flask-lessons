from flask import Flask, render_template, url_for, request

app = Flask(__name__)
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
        print(request.form)
    return render_template("contact.html", title="Обратная связь", menu=menu)


@app.route("/profile/<username>")
def profile(username: str):
    print(username)
    return ""


if __name__ == "__main__":
    app.run(debug=True)
