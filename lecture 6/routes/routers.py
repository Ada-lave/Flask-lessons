from flask import render_template, url_for, request, flash
from .user_routes import user_routes
menu = [
    {"name": "Установка", "url": "install-flask"},
    {"name": "Первое приложение", "url": "first-app"},
    {"name": "Обратная связь", "url": "contact"},
]

def register_routes(app):
    user_routes(app, menu)
    
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("page404.html", menu=menu, title="Ошибка")

    @app.route("/hellow")
    def hello():
        print(url_for("hello"))
        return "<h1>Hellow</h1>"


    @app.route("/")
    def index():
        return render_template("index.html", title="Про Flask", menu=menu)

