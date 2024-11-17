import math
import sqlite3
import time
from flask import url_for
import re


class LectureDB:
    def __init__(self, db):
        self.__db = db

    def get_menu(self):
        sql = """SELECT * FROM main_menu"""
        try:
            with sqlite3.connect(self.__db) as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute(sql)
                res = cur.fetchall()
                if res: 
                    return res
        except Exception as e:
            print(f"Ошибка чтения из базы: {e}")
        return []

    def add_post(self, title: str, text: str, url: str):
        try:
            with sqlite3.connect(self.__db) as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute(
                    f"SELECT COUNT() as `count` FROM posts WHERE url LIKE '{url}'"
                )
                res = cur.fetchone()

                if res["count"] > 0:
                    print("Статья уже есть")
                    return False
                tm = math.floor(time.time())
                base = url_for("static", filename="images_html")
                text = re.sub(
                    r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
                    "\\g<tag>" + base + "/\\g<url>>",
                    text,
                )
                cur.execute(
                    "INSERT INTO posts VALUES(NULL,?,?,?,?)", (title, text, url, tm)
                )
                con.commit()

        except sqlite3.Error as e:
            print(e)
            return False
        return True

    def get_post(self, alias: str):
        try:
            with sqlite3.connect(self.__db) as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute(
                    f"SELECT title, text FROM posts WHERE url = '{alias}' LIMIT 1"
                )
                res = cur.fetchone()
                if res:
                    base = url_for("static", filename="images_html")
                    text = re.sub(
                        r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
                        "\\g<tag>" + base + "/\\g<url>>",
                        res["text"],
                    )
                    return (res["title"], text)
        except sqlite3.Error as e:
            print(e)
        return (None, None)

    def get_posts(self):
        try:
            with sqlite3.connect(self.__db) as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute(f"SELECT id, title, url, text FROM posts")
                res = cur.fetchall()
                print(res)
                return res
        except sqlite3.Error as e:
            print(e)

        return []

    def add_user(self, name: str, email: str, hash: str) -> bool:
        try:
            with sqlite3.connect(self.__db) as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute(
                    f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'"
                )
                res = cur.fetchone()
                if res["count"] > 0:
                    print("Пользователь с таким email уже существует")
                    return False

                tm = math.floor(time.time())
                cur.execute(
                    "INSERT INTO users VALUES(NULL, ?, ?, ?, NULL, ?)",
                    (name, email, hash, tm),
                )
                con.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД " + str(e))
            return False
        # y4X-mSK-Wts-3ET

        return True
    
    def get_user(self, user_id: int):
        try:
            with sqlite3.connect(self.__db) as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
                res = cur.fetchone()
                if not res:
                    print("Пользователь не найден")
                    return False 

                return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))

        return False
    
    def get_user_by_email(self, email: str):
        try:
            with sqlite3.connect(self.__db) as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
                res = cur.fetchone()
                
                if not res:
                    return False
                
                return res
        except sqlite3.Error as e:
            print("Ошибка получения по email")
        
        return False
    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False
 
        try:
            with sqlite3.connect(self.__db) as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                binary = sqlite3.Binary(avatar)
                cur.execute(f"UPDATE users SET avatar = ? WHERE id = ?", (binary, user_id))
                con.commit()
        except sqlite3.Error as e:
            print("Ошибка обновления аватара в БД: "+str(e))
            return False
        return True