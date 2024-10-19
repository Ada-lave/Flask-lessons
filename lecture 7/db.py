import sqlite3
from flask import g


def get_db(app):
    if not hasattr(g, "link_db"):
        g.link_db = connect_db(app)
    return g.link_db


def connect_db(app):
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


def create_db(app):
    db = connect_db(app)
    with app.open_resource("sq_db.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()
