from flask import render_template, url_for, make_response, url_for, redirect, Flask
from .user_routes import user_routes
from .post_routes import post_routes
from db import get_db
from lecture_db import LectureDB

menu = [
    {"name": "Установка", "url": "install-flask"},
    {"name": "Первое приложение", "url": "first-app"},
    {"name": "Обратная связь", "url": "contact"},
]


def register_routes(app: Flask):
    user_routes(app, menu)
    post_routes(app)

    @app.errorhandler(404)
    def page_not_found(error):
        db = get_db(app)
        l_db = LectureDB(db)
        return ("Page not found", 404)

    
    @app.route('/redirect')
    def red():
        return redirect(url_for("index"), 301)

    @app.route("/")
    def index():
        db = get_db(app)
        l_db = LectureDB(db)
        content = render_template("index.html", title="Про Flask", menu=l_db.get_menu(), posts=l_db.get_posts())
        res = make_response(content)
        
        return res

    @app.before_request
    def before_request():
        print("before")
        
    
    @app.after_request
    def after_request(response):
        print("after")
        
        return response
    
    @app.teardown_request
    def teardown_request(response):
        print("teardown request")
        
        return response