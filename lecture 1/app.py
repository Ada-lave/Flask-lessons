from flask import Flask, render_template

app = Flask(__name__)


@app.route("/hellow")
def hello():
    return "<h1>Hellow</h1>"


@app.route("/")
def index():
    menu = ["О нас", "Установка", "Отзывы"]
    return render_template("index.html", title="Про Flask", menu=menu)


if __name__ == "__main__":
    app.run(debug=True)
