import math
import sqlite3
import time

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
    
    def add_post(self, title: str, text: str):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES(NULL,?,?,?)", (title, text, tm))
            self.__db.commit()
        
        except sqlite3.Error as e:
            print(e)
            return False
        return True

    def get_post(self, id: int):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE id = {id} LIMIT 1")
            res = self.__cur.fetchone()      
            return res
        except sqlite3.Error as e:
            print(e)
        return (None, None)

    def get_posts(self):
        try:
            self.__cur.execute(f"SELECT id, title, text FROM posts")
            res = self.__cur.fetchall()
            print(res)
            return res
        except sqlite3.Error as e:
            print(e)
        
        return []
        