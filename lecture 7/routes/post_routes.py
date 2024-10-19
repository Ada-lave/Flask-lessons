from flask import abort, render_template, url_for, request, flash, session, redirect
from db import get_db
from lecture_db import LectureDB

def post_routes(app):
    
    @app.route("/add_post", methods=["POST", "GET"])
    def add_post():
        db = get_db(app)
        l_db = LectureDB(db)
        
        if request.method == "POST":
            if len(request.form['name']) > 4 and len(request.form['post']) > 10:
                res = l_db.add_post(request.form['name'], request.form['post'])
                
                if not res:
                    flash("Ошибка добавления статьи", category="error")
                else:
                    flash("Успешно добавленно", category="success")
            else:
                    flash("Ошибка добавления статьи", category="error")
        
        return render_template("add_post.html", menu=l_db.get_menu(), title="Добавление статьи")
    
    @app.route("/posts/<int:id>")
    def show_post(id: int):
        db = get_db(app)
        l_db = LectureDB(db)
        title, post = l_db.get_post(id)
        
        if not title:
            abort(404)
    
        return render_template("show_post.html", menu=l_db.get_menu(), title=title, post=post)
