from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/hellow")
def hello():
    print(url_for("hello"))
    return "<h1>Hellow</h1>"


@app.route("/")
def index():
    menu = ["О нас", "Установка", "Отзывы"]
    return render_template("index.html", title="Про Flask", menu=menu)

@app.route("/profile/<username>")
def profile(username: str):
    print(username)
    return ""


if __name__ == "__main__":
    app.run(debug=True)
