import math
import sqlite3
import time
from flask import url_for
import re

class LectureDB:
    def __init__(self, db):
        self.__db = db
        self.__cur: sqlite3.Cursor = db.cursor()
        
    def get_menu(self):
        sql = '''SELECT * FROM main_menu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except Exception as e:
            print(f"Ошибка чтения из базы: {e}")
        return []
    
    def add_post(self, title: str, text: str, url: str):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM posts WHERE url LIKE '{url}'")
            res = self.__cur.fetchone()
            
            if res['count'] > 0:
                print("Статья уже есть")
                return False
            tm = math.floor(time.time())
            base = url_for("static", filename="images_html")   
            text = re.sub(
                r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>", 
                "\\g<tag>" + base + "/\\g<url>>", 
                text)
            self.__cur.execute("INSERT INTO posts VALUES(NULL,?,?,?,?)", (title, text, url, tm))
            self.__db.commit()
        
        except sqlite3.Error as e:
            print(e)
            return False
        return True

    def get_post(self, alias: str):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE url = '{alias}' LIMIT 1")
            res = self.__cur.fetchone()  
            if res:
                base = url_for("static", filename="images_html")   
                text = re.sub(
                    r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>", 
                    "\\g<tag>" + base + "/\\g<url>>", 
                    res['text'])
                return (res['title'], text)
        except sqlite3.Error as e:
            print(e)
        return (None, None)

    def get_posts(self):
        try:
            self.__cur.execute(f"SELECT id, title, url, text FROM posts")
            res = self.__cur.fetchall()
            print(res)
            return res
        except sqlite3.Error as e:
            print(e)
        
        return []
        